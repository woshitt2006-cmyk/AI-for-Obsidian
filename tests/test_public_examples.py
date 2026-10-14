import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from bridge import validate, plan_import, apply_plan

class PublicExampleTests(unittest.TestCase):
    def test_demo_graph_notes_and_canvas_references(self):
        demo=ROOT/'examples/demo-vault'
        graph=json.loads((demo/'_AIKG/graph.json').read_text(encoding='utf-8'))
        self.assertEqual(len(graph['nodes']),13);self.assertEqual(len(graph['edges']),16)
        validate(graph,{'nodes':[],'edges':[]})
        for n in graph['nodes']:
            self.assertTrue((demo/f'Concepts/{n["id"]}.md').is_file())
        for e in graph['edges']:
            self.assertTrue((demo/f'Relations/{e["id"]}.md').is_file())
        for p in (demo/'Canvas').glob('*.canvas'):
            c=json.loads(p.read_text(encoding='utf-8'))
            ids={n['id'] for n in c['nodes']}
            for n in c['nodes']:self.assertTrue((demo/n['file']).is_file())
            for e in c['edges']:self.assertIn(e['fromNode'],ids);self.assertIn(e['toNode'],ids)
        for p in demo.rglob('*.md'):
            text=p.read_text(encoding='utf-8')
            for target in re.findall(r'\[\[([^]|]+)',text):self.assertTrue((demo/(target+'.md')).exists(),str(p)+': '+target)
            if '<!-- AIKG:END -->' in text:
                self.assertEqual(text.split('<!-- AIKG:END -->')[1].strip(),'## 我的理解\n\n## 未解决问题')
        self.assertFalse((demo/'.obsidian').exists());self.assertFalse((demo/'_AIKG/bridge').exists());self.assertFalse((demo/'_AIKG/backups').exists())

    def test_schema_and_validator_contract(self):
        for version in ['1.0','1.1']:
            schema=json.loads((ROOT/f'schemas/knowledge-v{version}.schema.json').read_text(encoding='utf-8'))
            self.assertEqual(schema['properties']['schema_version']['const'],version)
            node=schema['properties']['nodes']['items'];edge=schema['properties']['edges']['items']
            self.assertEqual(set(node['properties']['type']['enum']),{'concept','theory','equation','method','application','question','paper'})
            self.assertEqual(set(edge['properties']['relation']['enum']),{'foundation','derive','application','analogy','extension','difference','prerequisite'})
            self.assertEqual('content_md' in node['required'],version=='1.1')
            self.assertEqual('detail_md' in edge['required'],version=='1.1')
        graph=json.loads((ROOT/'examples/demo-vault/_AIKG/graph.json').read_text(encoding='utf-8'))
        sample=json.loads((ROOT/'examples/phase2/sample_import.json').read_text(encoding='utf-8'))
        validate(sample,graph)

    def test_sample_import_preserves_fixture_and_repeats(self):
        demo=ROOT/'examples/demo-vault'
        before={p.relative_to(demo).as_posix():p.read_bytes() for p in demo.rglob('*') if p.is_file()}
        with tempfile.TemporaryDirectory() as temp:
            vault=Path(temp)/'public-vault';shutil.copytree(demo,vault)
            sample=ROOT/'examples/phase2/sample_import.json'
            plan=plan_import(vault,sample);apply_plan(plan)
            graph=json.loads((vault/'_AIKG/graph.json').read_text(encoding='utf-8'))
            self.assertEqual(len(graph['nodes']),14);self.assertEqual(len(graph['edges']),18)
            self.assertEqual(plan_import(vault,sample).writes,{})
        self.assertEqual(before,{p.relative_to(demo).as_posix():p.read_bytes() for p in demo.rglob('*') if p.is_file()})

    def test_local_document_links_and_prompt_context(self):
        for p in ROOT.rglob('*.md'):
            if '.git' in p.parts or 'my-vault' in p.parts:continue
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
                if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
                target=target.split('#',1)[0].split(' ',1)[0].strip('<>')
                if target:self.assertTrue((p.parent/target).exists(),str(p)+': '+target)
        ctx=json.loads((ROOT/'examples/phase2/prompt_context.json').read_text(encoding='utf-8'))
        note=ctx['selection']['note_file'];self.assertFalse(Path(note).is_absolute());self.assertNotIn('..',Path(note).parts)
        self.assertEqual(ctx['current_node']['id'],'finite_element_mesh')
        self.assertTrue((ROOT/'examples/phase2/full_prompt.md').stat().st_size>1000)

if __name__=='__main__':unittest.main()
