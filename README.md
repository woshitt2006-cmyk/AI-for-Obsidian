# AI Knowledge Graph Assistant

面向科研学习的个人知识网络工具：将 AI 回答整理成结构化 JSON，再导入 Obsidian Markdown 与 Canvas；从节点及一跳上下文生成下一次追问。

**当前阶段：Phase 2 本地 Bridge MVP。** Python 标准库实现，无 API 密钥、无运行时第三方包。命令行可跨平台使用；文件选择窗口仅支持 Windows。需要 Python 3.10+。

```text
提出问题 → AI 输出深度 Knowledge JSON → 预览/导入
    ↑                                      ↓
复制追问提示词 ← 节点及一跳上下文 ← Obsidian 知识地图
```

## 已完成

- v1.0/v1.1 协议校验：格式、字段、ID、枚举、关系端点、正文和来源结构。
- 增量合并：复用节点、追加正文、关系去重、身份和方向冲突报告。
- Obsidian 输出：完整节点笔记、关系解释笔记、双向链接、主题 Canvas。
- 内容保护：手写区与旧正文保留、Canvas 位置保留、重复导入幂等、备份和普通异常回滚。
- 本地追问：节点正文、手写记录、一跳关系和邻居摘要，生成提示词及上下文清单。
- Windows 工具窗口：选择文件、预览导入、选择节点、生成并复制提示词。
- 科研示例：相场断裂长度尺度主题，13 个节点、16 条候选关系，以及增量测试数据。

示例中的 AI 内容是学习与软件测试材料，仍需核实。候选与待调整状态保留，不因导入成功而升级为已确认知识。

## 五分钟试用

从仓库根目录运行。首先复制示例仓库为自己的工作副本，不在受版本控制的示例中积累个人笔记。

Windows PowerShell：

```powershell
Copy-Item -LiteralPath 'examples/demo-vault' -Destination 'my-vault' -Recurse
python bridge.py examples/phase2/sample_import.json --vault my-vault
python bridge.py examples/phase2/sample_import.json --vault my-vault --apply
```

macOS / Linux：

```bash
cp -R examples/demo-vault my-vault
python3 bridge.py examples/phase2/sample_import.json --vault my-vault
python3 bridge.py examples/phase2/sample_import.json --vault my-vault --apply
```

不带 `--apply` 的命令只预览。示例应新增 1 个“参考单元映射”节点和 2 条关系，总图变为 14 节点/18 关系。再次执行相同导入不重复追加。

在 Obsidian 选择“打开文件夹作为仓库”，打开 `my-vault`，再打开 `Canvas/phase_field_length_scale.canvas`。Markdown 文件与 Canvas 必须一起保留。

Windows 也可双击 **launch.cmd**。窗口默认指向示例仓库；日常使用请改选 `my-vault`。如果已有 Python Launcher，可用 `py -3` 代替 `python`。桌面窗口需要 Windows PowerShell 5.1 与 Windows Forms。

## 生成节点追问

```powershell
python query_builder.py finite_element_mesh --vault my-vault --question '为什么形函数导数需要转换到物理坐标？'
```

提示词与上下文清单写入 `my-vault/_AIKG/prompts/`。也可在窗口点击“生成节点追问…”，选择节点、填写问题、生成后复制。将完整提示词发给 AI，只保存返回 JSON 代码块，回到工具预览并导入。

工具不会自动读取 ChatGPT 回复或发送问题。Obsidian 内右键 Ask AI 属于后续 Phase 3。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

测试在临时目录执行，不修改示例和个人仓库。GitHub Actions 配置 Windows/Linux 与 Python 3.10/3.12；远端运行结果需上传后查看。

## 仓库结构

```text
bridge.py                   协议校验、合并、文件输出与事务
query_builder.py            节点与一跳上下文 → 追问
import_gui.ps1 / launch.cmd Windows 窗口入口
schemas/                    v1.0/v1.1 输入结构说明
tests/                      单元测试与示例完整性测试
examples/demo-vault/        无个人状态的学习示例
examples/phase2/            可导入的测试批次与完整提示词
docs/                       设计、进度、协议、使用和路线图
.github/                    CI、Issue 与 PR 模板
```

## 当前限制

- 每个仓库只管理一个 `topic_id`。稳定英文 ID 作为文件名，中文名称用于标题和链接别名。
- 采用正文追加策略，不自动解决新旧解释矛盾，不自动改写旧关系。
- 同名不同 ID、同 ID 改名/改类型需人工处理；不同拼写的同义词不会自动识别。
- 同类型反向有向边报告可能冲突，显式保留后仍待审阅；反向边不必然表示科学错误。
- 无 Obsidian 插件、API 调用、PDF 提取、向量检索、多用户同步。
- 普通写入异常可回滚；断电/强制结束需按备份清单恢复。导入过程中避免编辑目标文件。

## 文档与协作

- [当前成果总结](docs/PROJECT_STATUS.md)
- [使用与恢复说明](docs/USER_GUIDE.md)
- [系统架构](docs/ARCHITECTURE.md)
- [深度内容协议](docs/PROTOCOL.md)
- [阶段路线图](docs/ROADMAP.md)
- [贡献指南](CONTRIBUTING.md)
- [发布到 GitHub](docs/GITHUB_PUBLISH.md)

代码与原创项目文档采用 [MIT License](LICENSE)。外部参考文献只提供链接，不包含其 PDF 或全文转载，来源权利不因本项目许可而改变。科学示例保留来源与待审阅状态。
