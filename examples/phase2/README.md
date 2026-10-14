# Phase 2 验收样例

sample_import.json 是确定性导入测试数据，不冒充 AI 的真实返回。针对 demo-vault 工作副本，应新增 reference_element_mapping 一个节点与两条 prerequisite 关系，结果为 14 节点/18 关系。同批次再导入不追加。

full_prompt.md 是已填写的完整学习提示词，含已有节点注册表、当前正文、一跳关系和 v1.1 输出协议；question.txt 只是工具的问题框内容。prompt_context.json 记录使用的上下文，所有路径均相对化。

先导入示例后，已有 ID 注册表发生变化。再次发给 AI 前请用 query_builder.py 从工作副本重新生成，不继续使用旧快照。

验收：预览数正确、正文与公式可读、关系链接可解析、已有 Canvas 位置保留、手写记录保留、重复批次无写入。真实 AI 的新增数不要求与确定性例子一致。
