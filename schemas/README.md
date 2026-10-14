# 协议结构

schemas 描述输入批次的字段结构，不是本地 graph.json 所有运行元数据的规范。实际 bridge.validate 还检查唯一 ID、跨批次端点、自环、重复边、Windows 保留名与管理标记；这些不能仅靠本 schema 表达。

v1.0 不要求详细正文；v1.1 的节点必须有 content_md/sources，边必须有 detail_md/sources。未知附加字段可保留在输入回执，但导入器只采用允许的正文与基本字段，不信任 AI 提供的确认状态。

核心运行不依赖 jsonschema 包。校验器/Schema 对齐测试采用仓库内最小结构检查，额外跨平台验证可作为协作任务。
