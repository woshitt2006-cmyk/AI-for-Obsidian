import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bridge import BridgeError, plan_import, apply_plan, safe_path, START, END
from query_builder import build_prompt, save_prompt

def node(id,name=None,content=None):
    return dict(id=id,name=name or id,type='concept',description='摘要',domain=['学习'],content_md=content or '## 解释\n\n公式 $d_h=N_1d_1+N_2d_2$。',sources=[])

def batch(nodes=None,edges=None):
    return dict(schema_version='1.1',topic_id='test_topic',topic='学习问题',nodes=nodes or [node('node_a')],edges=edges or [])

def edge(a,b):
    return dict(source=a,target=b,relation='prerequisite',description='前置理解',detail_md='解释为什么需要先理解来源节点。',sources=[])

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.base=Path(self.temp.name)
        self.vault=self.base/'中文 仓库'; self.vault.mkdir(); self.input=self.base/'输入 数据.json'
    def tearDown(self): self.temp.cleanup()
    def write(self,data): self.input.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    def import_data(self,data):
        self.write(data); p=plan_import(self.vault,self.input); apply_plan(p); return p
    def snapshot(self): return {p.relative_to(self.vault).as_posix():p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}
    def test_preview_is_read_only_and_import_has_valid_files(self):
        self.write(batch([node('node_a'),node('node_b')],[edge('node_a','node_b')]))
        p=plan_import(self.vault,self.input); self.assertEqual(self.snapshot(),{})
        apply_plan(p)
        canvas=json.loads((self.vault/'Canvas/test_topic.canvas').read_text(encoding='utf-8'))
        self.assertEqual(len(canvas['nodes']),2); self.assertEqual(len(canvas['edges']),1)
        for n in canvas['nodes']: self.assertTrue((self.vault/n['file']).is_file())
    def test_repeat_is_idempotent(self):
        data=batch(); self.import_data(data); previous=self.snapshot()
        self.write(data); p=plan_import(self.vault,self.input); self.assertEqual(p.writes,{})
        apply_plan(p); self.assertEqual(previous,self.snapshot())
    def test_append_preserves_manual_content_and_canvas_position(self):
        self.import_data(batch()); note=self.vault/'Concepts/node_a.md'
        note.write_text(note.read_text(encoding='utf-8')+'手写公式 $x^2$ 与中文。\n',encoding='utf-8')
        cp=self.vault/'Canvas/test_topic.canvas'; canvas=json.loads(cp.read_text(encoding='utf-8')); canvas['nodes'][0]['x']=987; canvas['nodes'][0]['color']='3'; cp.write_text(json.dumps(canvas),encoding='utf-8')
        self.import_data(batch([node('node_a',content='补充内容'),node('node_b')],[edge('node_a','node_b')]))
        actual=note.read_text(encoding='utf-8'); self.assertIn('公式 $d_h=',actual); self.assertIn('补充内容',actual); self.assertTrue(actual.endswith('手写公式 $x^2$ 与中文。\n'))
        new=json.loads(cp.read_text(encoding='utf-8')); self.assertEqual(new['nodes'][0],canvas['nodes'][0])
    def test_managed_edit_blocks_import_without_changes(self):
        self.import_data(batch()); note=self.vault/'Concepts/node_a.md'; note.write_text(note.read_text(encoding='utf-8').replace('## 解释','## 修改过的解释'),encoding='utf-8')
        previous=self.snapshot(); self.write(batch([node('node_a',content='新内容')]))
        with self.assertRaises(BridgeError):plan_import(self.vault,self.input)
        self.assertEqual(previous,self.snapshot())
    def test_invalid_dangling_duplicate_and_path_rejected(self):
        examples=[batch(edges=[edge('node_a','unknown')]),batch([node('node_a'),node('node_a')]),batch([node('../escape')]),batch([node('con')])]
        for data in examples:
            self.write(data)
            with self.assertRaises(BridgeError):plan_import(self.vault,self.input)
            self.assertEqual(self.snapshot(),{})
        with self.assertRaises(BridgeError):safe_path(self.vault.resolve(),'../escape.md')
    def test_write_failure_rolls_back(self):
        self.import_data(batch()); previous=self.snapshot()
        self.write(batch([node('node_a',content='新内容'),node('node_b')],[edge('node_a','node_b')]))
        p=plan_import(self.vault,self.input)
        def fail_after_first(i):
            if i==1: raise OSError('simulated disk failure')
        with self.assertRaises(OSError):apply_plan(p,after_write=fail_after_first)
        after=self.snapshot()
        for rel,data in previous.items():self.assertEqual(after[rel],data)
        for rel in p.writes:
            if rel not in previous:self.assertFalse((self.vault/rel).exists(), rel)
        self.assertFalse((self.vault/'_AIKG/bridge/import.lock').exists())
    def test_preview_race_detected(self):
        self.import_data(batch()); self.write(batch([node('node_a',content='新内容')]))
        p=plan_import(self.vault,self.input); path=self.vault/'Concepts/node_a.md'; path.write_text(path.read_text(encoding='utf-8')+'用户新编辑',encoding='utf-8')
        with self.assertRaises(BridgeError):apply_plan(p)
        self.assertTrue(path.read_text(encoding='utf-8').endswith('用户新编辑'))
    def test_symmetric_relation_deduplicated(self):
        e=edge('node_a','node_b'); e['relation']='difference'
        self.import_data(batch([node('node_a'),node('node_b')],[e]))
        r=copy.deepcopy(e); r['source'],r['target']=r['target'],r['source']
        self.import_data(batch([node('node_a')],[r]))
        graph=json.loads((self.vault/'_AIKG/graph.json').read_text(encoding='utf-8')); self.assertEqual(len(graph['edges']),1)
        canvas=json.loads((self.vault/'Canvas/test_topic.canvas').read_text(encoding='utf-8')); self.assertEqual(len(canvas['edges']),1)
    def test_topic_and_identity_conflict(self):
        self.import_data(batch())
        data=batch([node('node_b',name='node_a')]); self.write(data)
        with self.assertRaises(BridgeError):plan_import(self.vault,self.input)
        data=batch();data['topic_id']='different_topic';self.write(data)
        with self.assertRaises(BridgeError):plan_import(self.vault,self.input)
    def test_reverse_conflict_requires_explicit_review(self):
        self.import_data(batch([node('node_a'),node('node_b')],[edge('node_a','node_b')]))
        self.write(batch([node('node_a')],[edge('node_b','node_a')]))
        previous=self.snapshot()
        with self.assertRaisesRegex(BridgeError,'方向冲突'):plan_import(self.vault,self.input)
        self.assertEqual(previous,self.snapshot())
        p=plan_import(self.vault,self.input,allow_reverse=True);apply_plan(p)
        graph=json.loads((self.vault/'_AIKG/graph.json').read_text(encoding='utf-8'))
        self.assertEqual(len(graph['edges']),2);self.assertEqual(graph['edges'][-1]['review_status'],'needs_revision')
        canvas=json.loads((self.vault/'Canvas/test_topic.canvas').read_text(encoding='utf-8'));self.assertEqual(len(canvas['edges']),2)
    def test_query_one_hop_direction_manual_and_limits(self):
        self.import_data(batch([node('node_a'),node('node_b'),node('node_c'),node('node_d')],[edge('node_b','node_a'),edge('node_a','node_c'),edge('node_c','node_d')]))
        p=self.vault/'Concepts/node_a.md';p.write_text(p.read_text(encoding='utf-8')+'人工疑问：为什么？',encoding='utf-8')
        before=self.snapshot();prompt,context=build_prompt(self.vault,'node_a','解释公式',1)
        self.assertEqual(before,self.snapshot());self.assertEqual(context['selection']['neighbor_total'],2)
        self.assertEqual([n['id'] for n in context['neighbors']],['node_b']);self.assertEqual(context['edges'][0]['source'],'node_b')
        self.assertIn('人工疑问',context['current_manual_notes']);self.assertNotIn('node_d',[n['id'] for n in context['neighbors']])
        paths=save_prompt(self.vault,'node_a',prompt,context);self.assertTrue(all(p.is_file() for p in paths))
        with self.assertRaises(BridgeError):build_prompt(self.vault,'unknown','解释')
    def test_query_truncation_keeps_valid_context(self):
        self.import_data(batch([node('node_a',content='内容'*10000)]))
        _,context=build_prompt(self.vault,'node_a','解释',max_context_chars=4000)
        self.assertTrue(context['selection']['content_truncated']);self.assertTrue(context['selection']['extra_truncation'])
        self.assertLessEqual(len(json.dumps(context,ensure_ascii=False,indent=2)),4000)
    def test_current_demo_migration_no_duplicate_canvas_edges(self):
        demo=Path(__file__).resolve().parents[1]/'examples/demo-vault'
        self.assertTrue(demo.is_dir(), 'Public demo fixture is required')
        for folder in ['Concepts','Questions','Literature','Relations','Canvas']:
            src=demo/folder
            if src.exists():shutil.copytree(src,self.vault/folder,dirs_exist_ok=True)
        (self.vault/'_AIKG').mkdir();shutil.copy2(demo/'_AIKG/graph.json',self.vault/'_AIKG/graph.json')
        graph=json.loads((self.vault/'_AIKG/graph.json').read_text(encoding='utf-8'))
        original_canvas=json.loads((self.vault/'Canvas/phase_field_length_scale.canvas').read_text(encoding='utf-8'))
        data=dict(schema_version='1.1',topic_id=graph['topic_id'],topic='后续问题',nodes=[node('test_new_node')],edges=[edge('finite_element_mesh','test_new_node')])
        self.import_data(data)
        canvas=json.loads((self.vault/'Canvas/phase_field_length_scale.canvas').read_text(encoding='utf-8'))
        self.assertEqual(canvas['nodes'][:-1],original_canvas['nodes'])
        self.assertEqual(canvas['edges'][:-1],original_canvas['edges'])
        self.assertEqual(len(canvas['edges']),len(original_canvas['edges'])+1)

if __name__=='__main__':unittest.main()
