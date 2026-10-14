# AI Knowledge Graph Assistant

项目设计文档 · 2026-10-14 · 状态：架构评估与 MVP 设计，尚未实现

## 1. 项目目标与动机

面向科研学习，建立 ChatGPT → 结构化知识 → Obsidian → 新问题的探索循环。传统聊天沿追问线性推进，本项目将前置理论、数学推导、应用、类比和未解决问题组织成可探索的网络。衡量价值的是有效连接与后续探索质量，而不是笔记数量。

ChatGPT 负责解释、提取概念、提出连接与探索路径；本地 Bridge 负责校验、合并、生成文件与构建追问上下文；Obsidian 负责长期存储和可视化。Codex 是开发与维护工具，不应成为每次导入必需的运行时。

## 2. 可行性与桌面端边界

| 环节 | MVP 处理方式 | 自动化边界 |
| --- | --- | --- |
| ChatGPT 输出知识 JSON | 使用固定提示词，用户复制到文件 | 提示词不能当作严格 Schema 保证，导入端必须校验 |
| ChatGPT 回复自动送入 Bridge | 用户保存 UTF-8 JSON | 当前查阅资料未建立可供本项目直接使用的普通聊天回复订阅接口，不将其设为依赖 |
| 读取本地 Vault | Bridge 显式接收 Vault 路径 | 普通聊天不能被假定具有任意本地目录访问权，需要工具集成 |
| 生成 Markdown 与 Canvas | 本地工具完成 | 可直接实施 |
| 点击节点自动 Ask AI | MVP 按节点 ID 生成提示词，用户粘贴 | 点击事件与上下文发送需要后续 Obsidian 插件 |
| API 自动生成 | 后续可选适配器 | Responses API 的 Structured Outputs 可约束输出结构，但仍需检查图关系和知识正确性 |
| ChatGPT MCP 集成 | 后续调研 | 官方存在插件与 MCP 路径；本地插件提交有资格限制，安装与接入条件须实际验证 |

这里的边界是 MVP 的工程假设，不是断言桌面端永远无法扩展。自动化能力应按目标安装、账户、插件环境实测。

## 3. MVP 范围与架构

工作流：

1. 用户在 ChatGPT 提问，获得解释和独立 JSON 数据块。
2. 用户将 JSON 保存为输入文件。
3. Bridge 校验并展示新增、更新、冲突清单。
4. 用户运行导入，生成笔记与主题 Canvas。
5. 用户选择节点 ID，Bridge 读取当前图及相关笔记，输出追问提示词。
6. 用户把提示词粘贴回 ChatGPT，获得下一批 JSON，再次导入。

架构：`JSON 文件 → Parser / Validator → Graph Merge → Markdown + Canvas`；`Graph + Notes + Node ID → Query Builder → Prompt 文件`。

第一版不包含后台监听、聊天抓取、自动发送、Obsidian 插件、向量数据库、多用户协作。无需 API 密钥即可完成闭环。先通过单轮与多轮学习实验，再决定是否引入 API 或 MCP。

## 4. 数据协议 v1

保留原设计的 topic、nodes、edges，增加版本与主题标识。每次输入是增量批次，只增补或更新显式提供的条目；缺失条目不表示删除。

```json
{
  "schema_version": "1.0",
  "topic_id": "phase_field_length_scale",
  "topic": "为什么相场断裂需要长度尺度参数？",
  "nodes": [
    {
      "id": "phase_field_fracture",
      "name": "相场断裂",
      "type": "method",
      "description": "利用连续相场变量描述裂纹演化的断裂模型。",
      "domain": ["断裂力学", "连续介质力学"]
    },
    {
      "id": "variational_method",
      "name": "变分法",
      "type": "method",
      "description": "通过泛函的驻值条件建立控制方程。",
      "domain": ["应用数学"]
    }
  ],
  "edges": [
    {
      "source": "variational_method",
      "target": "phase_field_fracture",
      "relation": "foundation",
      "description": "相场断裂可基于变分能量框架建立。"
    }
  ]
}
```

节点类型：concept、theory、equation、method、application、question、paper。

关系类型：foundation、derive、application、analogy、extension、difference、prerequisite。source → target 表示：source 是 target 的基础、source 推导出 target、source 应用于 target、source 与 target 类比、target 是 source 的扩展、source 与 target 有区别、source 是 target 的前置知识。类比和区别语义对称，存储时按 ID 排序去重；其他关系保留方向。

节点 ID 在整个 Vault 内稳定，使用小写英文、数字和下划线；名称变更不修改 ID。AI 扩展时必须提供已有 ID 清单。同名不同 ID 或同 ID 不同含义进入人工冲突清单，不能自动认定是同一概念。边以 source、target、relation 组成稳定键。

校验：版本、必填字段、字段类型、枚举、批次内 ID 唯一、边端点存在于当前批次或已有图。自环报错，循环关系允许。错误时不写 Vault。结构合法不意味着知识正确；AI 内容标记为待核实，不自动补造论文和参考文献。

## 5. Vault 与文件约定

```text
KnowledgeVault/
  Canvas/<topic_id>.canvas
  Concepts/<node_id>.md
  Questions/<node_id>.md
  Literature/<node_id>.md
  Projects/
  _AIKG/graph.json
  _AIKG/imports/<batch_id>.json
  _AIKG/backups/<batch_id>/
  _AIKG/prompts/
```

question 放入 Questions，paper 放入 Literature，其他节点放入 Concepts。Projects 保留给人工项目笔记。文件名使用稳定 ID，中文名称用于标题与链接别名。类型变化涉及移动文件，第一版报告冲突，不自动移动。

graph.json 保存规范化图、导入来源、批次与内容摘要，作为关系事实的唯一存储；Markdown 和 Canvas 是其视图。笔记人工内容是追问上下文的另一来源，不从自由文本反向推断图关系。这个轻量机器状态文件解决跨轮次身份与合并问题，Obsidian 仍是用户探索界面。

笔记包含 frontmatter（kg_id、kg_type、review_status），标题，以及生成区中的类型、描述、领域和带关系说明的相关节点。核心思想、数学表达、直觉解释、推导、未解决问题作为人工编辑区；输入没有提供的内容不自动臆造。

生成区用固定标记包围。重复导入不得重复创建节点或边；同 ID 的内容变化以原子方式更新生成区，保留人工区。生成区被手动修改时先报告冲突。写入前备份目标文件，记录清单；失败按清单恢复。路径必须位于指定 Vault 内，拒绝路径穿越和符号链接逃逸。

## 6. Canvas 设计

知识节点映射成 JSON Canvas 的 file 节点，字段为 id、type、x、y、width、height、file。边使用 id、fromNode、toNode、label；原设计中的 position、size、from、to 只是概念表达，不能直接写入 Canvas。

```json
{
  "nodes": [
    {"id": "phase_field_fracture", "type": "file", "x": 0, "y": 0, "width": 360, "height": 240, "file": "Concepts/phase_field_fracture.md"},
    {"id": "variational_method", "type": "file", "x": 480, "y": 0, "width": 360, "height": 240, "file": "Concepts/variational_method.md"}
  ],
  "edges": [
    {"id": "variational_method__foundation__phase_field_fracture", "fromNode": "variational_method", "toNode": "phase_field_fracture", "label": "理论基础"}
  ]
}
```

第一版每个主题独立 Canvas，采用确定性网格布局。增量导入保留已有节点坐标，只为新节点安排空位；不覆盖用户重新排列的位置。不做全部知识的无限大地图。笔记同时写出双向链接，使知识连接可在普通笔记导航中访问；完整关系类型与解释保存在 graph.json。

## 7. 追问机制

输入：节点 ID、用户探索意图、可选邻居数限制。

读取：当前节点、一跳入边与出边及解释、邻居摘要、当前笔记人工区。默认最多 12 个邻居，按稳定顺序选择，并说明截断情况；用户可调整。无需将整个 Vault 发送给 AI。

输出：可复制的提示词与所用上下文清单。提示词要求解释已有连接、区分已知与待核实、给出少量有价值的新连接，并使用同一 JSON 协议返回增量结果。已有节点复用 ID，新关系可连接已有节点。将笔记正文作为引用材料，不能作为工具执行指令。

## 8. 开发任务与阶段

Phase 1：手动验证。使用同一学习主题完成至少三轮提问、生成图和追问，判断连接是否帮助发现新问题。

Phase 2：本地 Python CLI。模块包括 parser.py、graph_store.py、markdown_generator.py、canvas_generator.py、query_builder.py、cli.py。正式实现时补充 JSON Schema、示例、README 与可复现测试。

预期命令接口（设计，尚不可执行）：

```text
python -m ai_knowledge_bridge validate input.json
python -m ai_knowledge_bridge import input.json --vault <path> --dry-run
python -m ai_knowledge_bridge import input.json --vault <path>
python -m ai_knowledge_bridge query variational_method --vault <path>
```

实现顺序：协议与校验 → 合并与冲突报告 → Markdown → Canvas → 追问 → 多轮验收。先在示例 Vault 验证，再接入真实 Vault。

Phase 3：Obsidian 插件提供节点命令或右键 Ask AI；先调用已验证的 Bridge 能力。可选 API 适配器自动获得结构化结果；ChatGPT 集成单独验证资格、工具调用与本地权限，不与核心文件处理耦合。

## 9. 验收与约束

- 示例 JSON 导入后，笔记和 Canvas 可在 Obsidian 打开，所有边和文件链接可解析。
- 同一输入导入两次，图与文件内容保持一致，不产生重复条目。
- 第二批增量扩展保留已有节点、人工笔记与 Canvas 坐标。
- 非法 JSON、未知类型、悬空端点和越界路径产生明确错误，Vault 无部分写入。
- 同名冲突与生成区人工修改进入冲突报告，不静默覆盖。
- 追问包含正确的一跳关系及解释，遵守上下文上限，能够支持下一次增量导入。
- 模拟写入失败可以恢复备份；真实 Obsidian 打开和点击链接需做人工验收。

所有数据使用 UTF-8。导入和查询离线运行；MVP 不监控剪贴板，不上传 Vault，不需要 API 密钥。部署前仍需选择真实 Vault 路径，当前文档不假定其位置。

## 10. 官方资料与结论依据

- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)：API 可使用 JSON Schema 约束输出；本设计仍校验端点、身份与语义。
- [OpenAI ChatGPT 开发入口](https://developers.openai.com/chatgpt)：提供插件与自定义 MCP 接入路径。
- [桌面插件提交说明](https://developers.openai.com/plugins/deploy/desktop-only)：本地执行插件及提交资格限制；不能据此推定当前用户已具备接入能力。
- [JSON Canvas 1.0 规范](https://jsoncanvas.org/spec/1.0/)：Canvas 节点、文件引用与边的准确字段。

建议先验证手动 JSON 传递闭环。闭环有学习价值后，再自动化最耗时的步骤；插件不是 MVP 的前提。
