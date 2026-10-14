"""Offline, append-first Knowledge JSON importer. Python 3.10+; standard library only."""
import argparse
import copy
import hashlib
import json
import os
import re
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

NODE_TYPES = {'concept', 'theory', 'equation', 'method', 'application', 'question', 'paper'}
RELATIONS = {'foundation', 'derive', 'application', 'analogy', 'extension', 'difference', 'prerequisite'}
LABELS = dict(foundation='理论基础', derive='推导', application='应用', analogy='类比', extension='扩展', difference='区别', prerequisite='前置知识')
START, END = '<!-- AIKG:START -->', '<!-- AIKG:END -->'

class BridgeError(Exception):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def fail(condition, message):
    if not condition:
        raise BridgeError(message)

def string(value, field):
    fail(isinstance(value, str) and bool(value.strip()), f'{field} 必须是非空字符串')

def identifier(value, field):
    string(value, field)
    fail(bool(re.fullmatch(r'[a-z][a-z0-9_]{0,95}', value)), f'{field} 需为小写英文开头的英文/数字/下划线，最长96字符')
    fail(value not in {'con','prn','aux','nul'} and not re.fullmatch(r'(com|lpt)[1-9]', value), f'{field} 使用了 Windows 保留名称')

def edge_key(e):
    a, b = e['source'], e['target']
    if e['relation'] in {'analogy', 'difference'}:
        a, b = sorted((a, b))
    return (a, b, e['relation'])

def relation_id(e):
    return 'rel_' + digest('|'.join(edge_key(e)).encode())[:16]

def sources_valid(value, field):
    fail(isinstance(value, list), f'{field} 必须是数组')
    for i,s in enumerate(value):
        fail(isinstance(s, dict), f'{field}[{i}] 必须是对象')
        for k in ['title','url','locator','supports']:
            string(s.get(k), f'{field}[{i}].{k}')
        fail(s['url'].startswith(('https://','http://')), f'{field}[{i}].url 只允许 HTTP(S)')

def validate(batch, existing):
    fail(isinstance(batch, dict), 'JSON 顶层必须是对象')
    fail(batch.get('schema_version') in {'1.0','1.1'}, 'schema_version 只能是 1.0 或 1.1')
    identifier(batch.get('topic_id'), 'topic_id')
    string(batch.get('topic'), 'topic')
    for k in ['nodes','edges']:
        fail(isinstance(batch.get(k), list), f'{k} 必须是数组')
    known={n['id'] for n in existing['nodes']}
    incoming=set()
    for i,n in enumerate(batch['nodes']):
        fail(isinstance(n,dict), f'nodes[{i}] 必须是对象')
        identifier(n.get('id'), f'nodes[{i}].id')
        fail(n['id'] not in incoming, f'批次内重复节点：{n["id"]}')
        incoming.add(n['id'])
        for k in ['name','description']:
            string(n.get(k), f'{n["id"]}.{k}')
        fail(n.get('type') in NODE_TYPES, f'{n["id"]}.type 不合法')
        fail(isinstance(n.get('domain'),list) and all(isinstance(s,str) and s.strip() for s in n['domain']), f'{n["id"]}.domain 必须是字符串数组')
        if batch['schema_version']=='1.1':
            string(n.get('content_md'), f'{n["id"]}.content_md')
            sources_valid(n.get('sources'), f'{n["id"]}.sources')
        elif 'content_md' in n:
            string(n['content_md'], f'{n["id"]}.content_md')
        for k in ['content_md','description','name']:
            fail(START not in n.get(k,'') and END not in n.get(k,''), '输入正文不能包含 AIKG 管理标记')
    keys=set()
    for i,e in enumerate(batch['edges']):
        fail(isinstance(e,dict), f'edges[{i}] 必须是对象')
        for k in ['source','target']:
            identifier(e.get(k), f'edges[{i}].{k}')
            fail(e[k] in known|incoming, f'悬空端点：{e[k]}')
        fail(e['source']!=e['target'], '不允许自环')
        fail(e.get('relation') in RELATIONS, f'edges[{i}].relation 不合法')
        string(e.get('description'), f'edges[{i}].description')
        key=edge_key(e)
        fail(key not in keys, f'批次内重复关系：{key}')
        keys.add(key)
        if batch['schema_version']=='1.1':
            string(e.get('detail_md'), f'edges[{i}].detail_md')
            sources_valid(e.get('sources'), f'edges[{i}].sources')
        for k in ['description','detail_md']:
            fail(START not in e.get(k,'') and END not in e.get(k,''), '输入正文不能包含 AIKG 管理标记')

def load_input(path):
    raw=Path(path).read_bytes()
    text=raw.decode('utf-8-sig').strip()
    # Accept a single fenced JSON block, never extract from an entire chat response.
    if text.startswith('```'):
        match=re.fullmatch(r'```(?:json)?\s*\n([\s\S]*?)\n```',text)
        fail(match is not None, '请只保存 JSON 或一个完整 JSON 代码块，不要包含回答正文')
        text=match.group(1)
    try:
        obj=json.loads(text)
    except json.JSONDecodeError as e:
        raise BridgeError(f'JSON 第 {e.lineno} 行、第 {e.colno} 列格式错误：{e.msg}。请检查公式反斜杠和换行转义。') from e
    return obj,raw

def safe_path(root, relative):
    rel=Path(relative)
    fail(not rel.is_absolute() and '..' not in rel.parts, f'非法目标路径：{relative}')
    p=root/rel
    try:
        p.resolve().relative_to(root)
    except ValueError:
        raise BridgeError(f'目标通过链接指向仓库外：{relative}')
    return p

def folder(n):
    return 'Questions' if n['type']=='question' else 'Literature' if n['type']=='paper' else 'Concepts'

def note_path(n):
    return f'{folder(n)}/{n["id"]}.md'

def source_text(items):
    if not items:
        return '本批未提供来源；AI 内容待人工核实。'
    return '\n'.join(f'- [{s["title"]}]({s["url"]}) · {s["locator"]}：{s["supports"]}' for s in items)

def merge_sources(a,b):
    result=copy.deepcopy(a)
    for item in b:
        if item not in result: result.append(copy.deepcopy(item))
    return result

def add_section(text, section):
    fail(text.count(START)==1 and text.count(END)==1 and text.index(START)<text.index(END), '已有笔记缺少唯一有效管理区；请手动处理文件冲突')
    pos=text.index(END)
    return text[:pos].rstrip()+'\n\n'+section.strip()+'\n'+text[pos:]

@dataclass
class Plan:
    root: Path
    writes: dict
    before: dict
    summary: list
    batch_hash: str

def plan_import(vault, input_path, allow_reverse=False):
    root=Path(vault).resolve()
    fail(root.is_dir(), '请选择已存在的 Obsidian 仓库文件夹')
    batch, raw=load_input(input_path)
    graph_rel='_AIKG/graph.json'
    gp=safe_path(root,graph_rel)
    original_graph=gp.read_bytes() if gp.exists() else None
    graph=json.loads(original_graph.decode('utf-8-sig')) if original_graph is not None else dict(schema_version='1.1',topic_id=batch.get('topic_id'),topic=batch.get('topic'),nodes=[],edges=[])
    fail(isinstance(graph,dict) and isinstance(graph.get('nodes'),list) and isinstance(graph.get('edges'),list), '已有 graph.json 损坏')
    # Validate local identities before using them in paths.
    for n in graph['nodes']:
        identifier(n.get('id'),'已有节点 ID'); fail(n.get('type') in NODE_TYPES,'已有节点类型无效')
    fail(len({n['id'] for n in graph['nodes']})==len(graph['nodes']),'已有图含重复节点')
    validate(batch, graph)
    # Reverse directions can be valid, but need explicit review for the same directed relation.
    incoming_keys={edge_key(e) for e in batch['edges']}
    existing_keys={edge_key(e) for e in graph['edges']}
    reverse_candidates=[]
    for e in batch['edges']:
        if e['relation'] in {'analogy','difference'}: continue
        reverse=(e['target'],e['source'],e['relation'])
        if reverse in existing_keys|incoming_keys and edge_key(e) not in existing_keys:
            reverse_candidates.append(e)
    fail(not reverse_candidates or allow_reverse,
         '发现可能的关系方向冲突（不会自动合并或反转）：\n'+
         '\n'.join(f'{e["source"]} → {e["target"]} [{e["relation"]}]，同时存在反向关系' for e in reverse_candidates)+
         '\n请检查 JSON 的方向；若确认两条都应保留，可选择“保留已审阅的反向候选”。不同方向不必然意味着知识矛盾。')
    fail(graph['topic_id']==batch['topic_id'], '当前工具每个仓库只管理一个主题。topic_id 不一致，请选择另一个示例仓库')
    h=digest(encoded(batch))
    receipt_rel=f'_AIKG/bridge/imports/{h}.json'
    if safe_path(root,receipt_rel).exists():
        return Plan(root,{}, {}, ['这批 JSON 已导入；不重复追加正文、节点或关系。'],h)
    graph=copy.deepcopy(graph)
    nodes={n['id']:n for n in graph['nodes']}
    edges={edge_key(e):e for e in graph['edges']}
    fail(len(edges)==len(graph['edges']), '已有图含语义重复关系，请先审阅')
    state_rel='_AIKG/bridge/state.json'
    sp=safe_path(root,state_rel)
    state=json.loads(sp.read_text(encoding='utf-8')) if sp.exists() else {'files':{}}
    fail(isinstance(state.get('files'),dict),'导入状态损坏')
    writes={}; before={graph_rel:original_graph}; summary=[]; additions={}; new_node_ids=[]; new_edge_ids=[]

    def read(rel):
        p=safe_path(root,rel)
        data=p.read_bytes() if p.exists() else None
        before.setdefault(rel,data)
        if data is not None:
            fail(p.is_file(), f'文件路径被目录占用：{rel}')
            text=data.decode('utf-8-sig')
            if rel.endswith('.md'):
                fail(text.count(START)==1 and text.count(END)==1 and text.index(START)<text.index(END),f'文件冲突（管理区无效）：{rel}')
                managed=text[text.index(START):text.index(END)+len(END)]
                previous=state['files'].get(rel)
                if previous:
                    fail(digest(managed.replace('\r\n','\n').encode())==previous,f'生成区被手动修改：{rel}。请把修改移到人工区，再重新预览')
            return text
        return None

    for incoming in batch['nodes']:
        nid=incoming['id']
        for existing in graph['nodes']:
            fail(existing['id']==nid or existing['name']!=incoming['name'], f'同名不同 ID：{incoming["name"]}，请明确身份后重试')
        old=nodes.get(nid)
        if old:
            fail(old['type']==incoming['type'],f'节点 {nid} 类型变化，请先人工处理文件迁移')
            fail(old['name']==incoming['name'],f'节点 {nid} 名称变化，请先确认概念身份')
            content=incoming.get('content_md','')
            if content and content.strip() not in old.get('content_md',''):
                section='## 本次追问补充\n\n'+content+'\n\n### 本次来源\n\n'+source_text(incoming.get('sources',[]))
                additions.setdefault(nid,[]).append(section)
                old['content_md']=old.get('content_md','').rstrip()+'\n\n'+section
                summary.append(f'追加节点正文：{incoming["name"]}')
            elif old.get('description')!=incoming['description']:
                additions.setdefault(nid,[]).append('## 本次摘要补充\n\n'+incoming['description'])
            old['description']=incoming['description']
            old['domain']=list(dict.fromkeys(old.get('domain',[])+incoming['domain']))
            old['sources']=merge_sources(old.get('sources',[]),incoming.get('sources',[]))
        else:
            n={k:copy.deepcopy(incoming[k]) for k in ['id','name','type','description','domain','content_md','sources'] if k in incoming}
            n['review_status']='pending_human_review'; graph['nodes'].append(n); nodes[nid]=n; new_node_ids.append(nid)
            summary.append(f'新增节点：{n["name"]}')
        if batch['schema_version']=='1.0': summary.append(f'提示：{nid} 使用 v1.0，可能缺少详细正文')

    for incoming in batch['edges']:
        key=edge_key(incoming); old=edges.get(key)
        e=old or {k:copy.deepcopy(incoming[k]) for k in ['source','target','relation','description','detail_md','sources'] if k in incoming}
        if not old:
            e['id']=relation_id(e); e['review_status']='needs_revision' if incoming in reverse_candidates else 'provisional'; graph['edges'].append(e); edges[key]=e; new_edge_ids.append(e['id'])
            if incoming in reverse_candidates:
                e['review_notes']='用户显式选择保留反向候选，需核实双向语义。'
                summary.append(f'保留反向候选：{e["source"]} → {e["target"]}（待审阅）')
        else:
            fail(isinstance(e.get('id'),str) and re.fullmatch(r'rel_[a-z0-9_]+',e['id']), '已有关系没有有效 ID；需先迁移旧版 v1.0 图')
        rel=f'Relations/{e["id"]}.md'; current=read(rel)
        if not old:
            fail(current is None,f'新关系文件已存在，拒绝覆盖：{rel}')
            section=f'关系：`{e["relation"]}` · 状态：`{e["review_status"]}`\n\n## 摘要\n\n{e["description"]}\n\n## 为什么相连\n\n'+e.get('detail_md',e['description'])+'\n\n## 来源\n\n'+source_text(e.get('sources',[]))
            if e.get('review_notes'): section+='\n\n## 审阅说明\n\n'+e['review_notes']
            current=f'# {nodes[e["source"]]["name"]} → {nodes[e["target"]]["name"]}\n\n{START}\n'+section+f'\n{END}\n\n## 我的理解与修订\n\n'
            summary.append(f'新增关系：{nodes[e["source"]]["name"]} → {nodes[e["target"]]["name"]}（{LABELS[e["relation"]]}）')
        else:
            fail(current is not None, f'已有关系笔记丢失：{rel}')
            detail=incoming.get('detail_md','')
            if detail and detail.strip() not in e.get('detail_md',''):
                section='## 本次关系补充\n\n'+detail+'\n\n### 本次来源\n\n'+source_text(incoming.get('sources',[]))
                current=add_section(current,section)
                e['detail_md']=e.get('detail_md','').rstrip()+'\n\n'+section
                summary.append(f'追加关系正文：{e["id"]}')
            elif e['description']!=incoming['description']:
                current=add_section(current,'## 本次关系摘要\n\n'+incoming['description'])
            e['description']=incoming['description']; e['sources']=merge_sources(e.get('sources',[]),incoming.get('sources',[]))
        for end in ['source','target']:
            nid=e[end]; other=e['target'] if end=='source' else e['source']
            link=f'- [[{note_path(nodes[other])[:-3]}|{nodes[other]["name"]}]] · `{e["relation"]}` · [[Relations/{e["id"]}|阅读完整关系解释]]（{e["review_status"]}）'
            additions.setdefault(nid,[]).append(link)
        endpoint_links=f'[[{note_path(nodes[e["source"]])[:-3]}|来源节点]] · [[{note_path(nodes[e["target"]])[:-3]}|目标节点]]'
        if note_path(nodes[e['source']])[:-3] not in current:
            current=add_section(current,'## 端点\n\n'+endpoint_links)
        writes[rel]=current.encode('utf-8')

    affected=set(new_node_ids)|set(additions)
    for nid in affected:
        n=nodes[nid]; rel=note_path(n); current=read(rel)
        if nid in new_node_ids:
            fail(current is None,f'新节点笔记文件已存在，拒绝覆盖：{rel}')
            current=f'---\nkg_id: {nid}\nkg_type: {n["type"]}\nreview_status: pending_human_review\n---\n\n# {n["name"]}\n\n{START}\n## 摘要\n\n{n["description"]}\n\n'+n.get('content_md','正文待补充。')+'\n\n## 来源\n\n'+source_text(n.get('sources',[]))+f'\n{END}\n\n## 我的理解\n\n## 未解决问题\n\n'
        else:
            fail(current is not None,f'已有节点笔记丢失：{rel}')
        pieces=[]
        for piece in additions.get(nid,[]):
            if piece.startswith('- [['):
                target=re.search(r'\[\[Relations/([^]|]+)',piece).group(1)
                if f'[[Relations/{target}' in current: continue
            pieces.append(piece)
        if pieces: current=add_section(current,'\n\n'.join(pieces))
        writes[rel]=current.encode('utf-8')

    canvas_rel=f'Canvas/{batch["topic_id"]}.canvas'; cp=safe_path(root,canvas_rel)
    text=read(canvas_rel); canvas=json.loads(text) if text else {'nodes':[],'edges':[]}
    fail(isinstance(canvas.get('nodes'),list) and isinstance(canvas.get('edges'),list),'Canvas 格式损坏')
    cids={n['id'] for n in canvas['nodes']}
    fail(len(cids)==len(canvas['nodes']),'Canvas 节点 ID 重复')
    bottom=max((n['y']+n['height'] for n in canvas['nodes']),default=-160)
    count=0
    for n in graph['nodes']:
        if n['id'] not in cids:
            canvas['nodes'].append(dict(id=n['id'],type='file',file=note_path(n),x=(count%3)*500,y=bottom+160+(count//3)*420,width=420,height=300)); cids.add(n['id']); count+=1
    for e in graph['edges']:
        # Existing legacy edge IDs are preserved; identify them by endpoints and label type.
        endpoints={(e['source'],e['target'])}
        if e['relation'] in {'analogy','difference'}: endpoints.add((e['target'],e['source']))
        aliases={e['relation'],LABELS[e['relation']]}
        if e['relation']=='derive': aliases.add('引入/推导')
        if e['relation']=='prerequisite': aliases.add('前置理解')
        equivalents=[c for c in canvas['edges'] if (c['fromNode'],c['toNode']) in endpoints and (c.get('id')==e.get('id') or any(c.get('label','').startswith(a) for a in aliases))]
        if equivalents: continue
        label=LABELS[e['relation']]+' · '+('待调整' if e.get('review_status')=='needs_revision' else '候选')
        canvas['edges'].append(dict(id=e.get('id',relation_id(e)),fromNode=e['source'],toNode=e['target'],label=label,color='1' if e.get('review_status')=='needs_revision' else '5'))
    fail(len({e['id'] for e in canvas['edges']})==len(canvas['edges']),'Canvas 边 ID 冲突')
    for cn in canvas['nodes']:
        if cn.get('type')=='file':
            p=safe_path(root,cn['file']); fail(p.is_file() or cn['file'] in writes,f'Canvas 引用丢失：{cn["file"]}')
    fail(all(e['fromNode'] in cids and e['toNode'] in cids for e in canvas['edges']),'Canvas 存在悬空关系')
    writes[canvas_rel]=encoded(canvas)
    graph['schema_version']='1.1'
    writes[graph_rel]=encoded(graph)
    read(graph_rel); read(state_rel); read(receipt_rel)
    receipt={'batch_hash':h,'topic_id':batch['topic_id'],'summary':summary,'original':batch}
    writes[receipt_rel]=encoded(receipt)
    writes[f'_AIKG/bridge/imports/{h}.original.json']=raw
    read(f'_AIKG/bridge/imports/{h}.original.json')
    # Only changed bytes need writing. Baselines cover managed text; manual suffix remains editable.
    for rel,data in list(writes.items()):
        if rel.endswith('.md'):
            txt=data.decode('utf-8'); managed=txt[txt.index(START):txt.index(END)+len(END)]
            state['files'][rel]=digest(managed.replace('\r\n','\n').encode())
        if rel not in before: read(rel)
        if before[rel]==data: del writes[rel]
    writes[state_rel]=encoded(state)
    summary.append(f'预览：{len(new_node_ids)} 个新节点、{len(new_edge_ids)} 条新关系；总图 {len(graph["nodes"])} 节点/{len(graph["edges"])} 关系。')
    if not sp.exists(): summary.append('首次接入：保留已有管理区，今后记录其指纹；本次只追加内容。')
    summary.append('AI 内容均保持待审阅；工具不判断公式与关系是否正确。')
    return Plan(root,writes,before,summary,h)

def apply_plan(plan, after_write=None):
    if not plan.writes: return None
    root=plan.root
    for rel,data in plan.before.items():
        p=safe_path(root,rel); current=p.read_bytes() if p.exists() else None
        fail(current==data,f'预览后文件发生变化：{rel}。请重新预览')
    lock=safe_path(root,'_AIKG/bridge/import.lock'); lock.parent.mkdir(parents=True,exist_ok=True)
    try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError: raise BridgeError('另一导入正在运行或上次异常退出留下 import.lock。先确认没有导入进程，参阅 README 恢复步骤')
    os.close(fd)
    backup_rel='_AIKG/bridge/backups/'+datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8]
    backup=safe_path(root,backup_rel); backup.mkdir(parents=True)
    manifest={'status':'preparing','files':[]}; touched=[]; temporary=[]
    try:
        for rel in plan.writes:
            data=plan.before.get(rel)
            if data is not None:
                dest=backup/'files'/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
            manifest['files'].append({'path':rel,'existed':data is not None})
        (backup/'manifest.json').write_bytes(encoded(manifest))
        manifest['status']='applying'; (backup/'manifest.json').write_bytes(encoded(manifest))
        for i,(rel,data) in enumerate(plan.writes.items()):
            p=safe_path(root,rel)
            current=p.read_bytes() if p.exists() else None
            fail(current==plan.before.get(rel),f'写入前文件变化：{rel}')
            p.parent.mkdir(parents=True,exist_ok=True)
            temp=p.with_name(p.name+'.bridge_'+uuid.uuid4().hex+'.tmp'); temporary.append(temp)
            temp.write_bytes(data); temp.replace(p); touched.append(rel)
            if after_write: after_write(i)
        manifest['status']='complete'; (backup/'manifest.json').write_bytes(encoded(manifest))
    except Exception:
        for rel in reversed(touched):
            p=safe_path(root,rel); previous=plan.before.get(rel)
            if previous is None: p.unlink(missing_ok=True)
            else: p.write_bytes(previous)
        manifest['status']='rolled_back'; (backup/'manifest.json').write_bytes(encoded(manifest))
        raise
    finally:
        for p in temporary: p.unlink(missing_ok=True)
        lock.unlink(missing_ok=True)
    return backup

def cli():
    parser=argparse.ArgumentParser(description='Knowledge JSON → Obsidian，默认追加正文并保留旧内容')
    parser.add_argument('input',help='UTF-8 JSON 文件路径')
    parser.add_argument('--vault',required=True,help='Obsidian 仓库文件夹')
    parser.add_argument('--apply',action='store_true',help='执行导入；不指定时只预览')
    parser.add_argument('--allow-reverse',action='store_true',help='显式保留已人工审阅的反向候选，仍标记待审阅')
    args=parser.parse_args()
    try:
        plan=plan_import(args.vault,args.input,args.allow_reverse)
        print('\n'.join(plan.summary))
        if args.apply:
            backup=apply_plan(plan)
            print('导入完成。备份：'+str(backup) if backup else '没有重复写入。')
        else: print('未写入仓库。确认后增加 --apply 执行。')
    except (BridgeError,OSError,ValueError,KeyError,TypeError) as e:
        print('导入失败：'+str(e),file=sys.stderr); return 1
    return 0

if __name__=='__main__':
    raise SystemExit(cli())
