# AI Knowledge Bridge

这是一个离线本地导入工具：将 ChatGPT 的 Knowledge JSON 导入 Obsidian。支持 v1.0/v1.1，无 API 密钥和第三方 Python 包。详细正文保留在节点笔记，关系正文放在 Relations 中；工具不会判断物理内容或自动纠正关系。

## Windows 操作

首先复制 examples/demo-vault 为 my-vault 工作副本，日常使用请选择副本。

1. 将 AI 输出的 JSON 代码块内容复制到记事本，另存为 `next_question.json`。编码选 UTF-8，保存类型选“所有文件”，避免成为 `.json.txt`。可以保存一个完整 JSON 代码块；不要把代码块外的直接解释也复制进去。
2. 双击本目录的 **launch.cmd**。窗口使用 Windows 自带组件；需要 Python 3.10+；可通过 AIKG_PYTHON 选择解释器，也可探测可用的 Codex 运行时、Python Launcher 或 PATH。启动脚本只对本次进程使用 ExecutionPolicy Bypass，不修改系统执行策略。
3. 点击“选择…”选择 JSON 文件。首次仓库默认指向仓库 examples/demo-vault，也可以选择实际仓库的根目录（含 Concepts、Canvas 的那一层）。
4. 点击“检查并预览”，查看新增节点、关系和追加内容。
5. 点击“导入到仓库”。工具先备份，再执行写入。打开 Obsidian 的主题 Canvas；索引未刷新时重启 Obsidian。

可以把工具文件夹移到 Documents 下的其他位置，重新选择仓库即可。无需每次把 JSON 发给 Codex。支持中文和含空格的文件路径。运行时只在工具目录保存所选仓库路径，在仓库 _AIKG/bridge 中保存导入状态与备份。

## 更新与内容保护

默认追加正文，避免 AI 的短回答替换已有长笔记。已有节点复用 ID；没有返回的条目不会删除。相同批次不会重复导入；同一关系以端点和类型去重，analogy/difference 对称去重。

修改已有摘要会追加摘要记录；修改正文会追加本次内容，不自动删除旧解释。因此新内容与旧内容可能矛盾，仍需人工审阅。工具不会按语义合并两篇解释，也不会将新关系自动改成其他类型。

“我的理解”和管理标记外的正文可以自由编辑。工具首次接入旧仓库时保留当前生成区作为基线，以后若管理区被人工修改，会报告冲突。请将修改移到人工区，并将管理区恢复为上次备份内容后重试；不要直接删除状态文件绕过冲突。

同名不同 ID、同 ID 改名或改变类型会阻止导入，需先确认身份/文件迁移。v1.1 输入的每个节点须有 content_md/sources，每条边须有 detail_md/sources；空 sources 允许但表示待核实。不允许 AI 输入中的 review_status 自动将内容变成已确认。

同类型有向关系的新反向边会报告可能的方向冲突；这不等于数学上一定矛盾。先检查输入 JSON。如果确实要保留双向关系，勾选“保留已审阅的反向候选”后重新预览；两条边分别保留，新边仍标记待审阅。analogy/difference 的反向会按对称关系去重。

当前 MVP 每个仓库管理一个 topic_id。主题名称 topic 可以改变，topic_id 必须固定。旧 v1.0 数据可导入；没有稳定关系 ID 的旧本地图需先迁移，examples/demo-vault 已兼容。

## 命令行

```powershell
python .\bridge.py 'C:\path\next_question.json' --vault 'C:\path\KnowledgeVault'
python .\bridge.py 'C:\path\next_question.json' --vault 'C:\path\KnowledgeVault' --apply
```

第一条只预览，第二条执行。也可把 `python` 换成 `py -3` 或 Python 的绝对路径。

## 从节点生成追问

在窗口中选择仓库，点击“生成节点追问…”。选择节点名称，填写不理解的段落或问题，点击“生成追问文件”，查看内容后点击“复制提示词”，粘贴到 ChatGPT。得到 JSON 后回到导入窗口，完成预览与导入。

提示词读取当前节点详细正文、管理区之后的人工记录、一跳入边/出边解释与邻居摘要，并保留候选状态。默认最多 12 个邻居，按 ID 稳定排序；过长正文截断时明确记录。整个上下文默认限制为 16000 字符，生成文件附带 context.json 清单。它没有自动发送功能，也没有从 Obsidian 点击事件直接触发。

```powershell
python .\query_builder.py finite_element_mesh --vault 'C:\path\KnowledgeVault' --question '为什么梯度公式成立？'
```

文件保存在仓库 `_AIKG/prompts/` 中。命令行可用 `--max-neighbors` 和 `--max-context-chars` 调整范围。当前不支持由整篇 PDF 提取节点，也不推断没有保存的历史学习路径。

## 备份与异常恢复

备份位于 `_AIKG/bridge/backups/<时间_ID>/`，包含 files 下的旧文件和 manifest.json 清单。普通写入异常会自动恢复本次写入；遇到断电/强制结束不能保证自动回滚。避免导入时在 Obsidian 编辑目标文件。

如果异常退出留下 `_AIKG/bridge/import.lock`：先确认导入工具已经关闭；检查最新备份 manifest 的 status。若为 preparing/applying，先按清单把 existed=true 的备份文件恢复到对应位置，把 existed=false 的本次新文件移到仓库外的临时目录；确认恢复后移除锁文件再导入。status=complete 表示事务已完成。恢复后保留备份供核对。

Canvas 原有节点位置、尺寸、线条样式保留，新节点放在已有地图下方。只能保证已检查的本地文件结构，不包含 Obsidian UI 自动验收。若你重命名了机器管理笔记或改了 Canvas 指向，应先修复路径；工具不会猜测移动位置。

## 文件

- import_gui.ps1：Windows 文件选择与预览窗口。
- bridge.py：协议校验、合并、笔记/Canvas 生成、备份与回滚。
- query_builder.py：节点、一跳关系、人工记录 → 深度追问提示词和上下文清单。
- launch.cmd：Windows 启动入口。
- tests/test_bridge.py：重复导入、保护、冲突和失败恢复等测试。

旧 work/ 实验脚本已被此工具替代，不要继续运行它们覆盖新图谱。
