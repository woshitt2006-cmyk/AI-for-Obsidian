# 深度学习内容协议 v1.1

## 为什么需要调整

v1 的 description 是摘要，用它直接生成全文必然得到索引卡片。后续每轮同时输出可合并的图结构和可阅读的 Markdown 正文；导入器负责保存和链接，不承担凭摘要猜测、扩写知识的职责。

现有 ID、类型、关系枚举保持不变。v1.1 新增节点 content_md、边 detail_md，以及分别附带的 sources。旧批次仍保留；没有正文的旧条目可读取，但标记内容待补充。发送的新节点与实质更新的节点必须有正文，边同理；缺失条目不表示删除。

## 字段示例

```json
{
  "schema_version": "1.1",
  "topic_id": "phase_field_length_scale",
  "topic": "本轮探索问题",
  "nodes": [
    {
      "id": "crack_surface_energy",
      "name": "Griffith裂纹表面能",
      "type": "equation",
      "description": "用新增裂纹面积对应的能量代价描述断裂阻力。",
      "domain": ["断裂力学"],
      "content_md": "## 核心问题\n\n这里放完整解释。\n\n## 数学表达\n\n$$\nW_c=\\int_{\\Gamma}G_c\\,\\mathrm{d}A\n$$\n\n这里解释每个符号、适用条件与例子。",
      "sources": [
        {
          "title": "An assessment of phase field fracture: crack initiation and growth",
          "url": "https://arxiv.org/html/2103.05443v2",
          "locator": "2.1 节，公式 1–3",
          "supports": "Griffith 能量与相场正则化之间的联系"
        }
      ]
    }
  ],
  "edges": [
    {
      "source": "crack_surface_energy",
      "target": "phase_field_fracture",
      "relation": "foundation",
      "description": "Griffith 裂纹面积能量为相应变分相场模型提供目标能量。",
      "detail_md": "## 为什么相连\n\n完整说明从尖锐裂纹表面积分到扩散体积分的过程，并明确模型范围。\n\n## 如何使用这条联系\n\n说明它如何帮助回答本轮问题。",
      "sources": []
    }
  ]
}
```

JSON 中的换行写成 `\n`，LaTeX 反斜杠写成 `\\`。保存到 Markdown 后恢复实际换行和单个反斜杠，不将转义文本直接展示。这里只是字段示例，不是完整学习正文的合格样本。

## 正文深度要求

节点正文应能独立回答“是什么、为什么、怎么用、何时不适用”。通常组织为核心问题、直觉、公式与符号、推导或机制、具体例子、适用范围、常见误解、下一问。概念不必硬凑公式；公式节点必须解释符号和条件。篇幅服从理解需要，通常 600–1200 中文字，困难节点可以更长。篇幅是建议，不能仅按字数验收。

关系正文通常 250–600 中文字，解释两个节点怎样相连、通过什么中间步骤、方向为什么这样、在什么条件下成立、如何用于当前问题。若标签不合适，正文明确指出，不用长篇文字掩盖错误连线。模型限定、未核实结论、教学推演与来源直接陈述需区分。

对于 v1 未能表示的 controls、specialization、limit 等关系，在 JSON 外报告修改建议，当前枚举不擅自扩充。先解决语义一致性，再决定下一版本。

## Obsidian 表现

节点仍使用 Concepts/<id>.md。摘要用于 Canvas 卡片的快速浏览，全文在笔记内阅读。关系存放于 Relations/<稳定关系ID>.md；两个端点笔记都提供该关系的链接。Canvas 连线只显示短标签，完整解释不塞进连线。关系笔记不自动加入主地图，以免地图节点数量翻倍。

graph.json 保存 content_md/detail_md/sources，生成 Markdown 时仅更新机器管理区，人工区保留。sources 说明支持范围，空数组表示未提供可核查来源；不自动把 AI 生成视为验证完成。

## 可复制的内容补全提示词

```text
请把已有图谱升级为可独立学习的内容。不要只给节点摘要。

下面我会提供已有 JSON 和本轮目标。使用 schema_version="1.1"，保留 topic_id 和所有稳定 ID。沿用 v1 的节点与关系枚举，不创建同义重复节点。

每个补全节点输出 id、name、type、description、domain、content_md、sources。
description 是短摘要。content_md 是完整 Markdown 学习正文，包含核心问题、直觉、必要的公式及逐一符号解释、推导或机制、例子、适用条件、常见误解、后续问题。概念节点不硬凑公式。正文应达到可以独立阅读、理解、使用的程度；通常 600–1200 中文字，按难度调整。

每个补全关系输出 source、target、relation、description、detail_md、sources。
detail_md 解释为什么相连、连接的中间步骤、方向与适用条件、能解决什么问题，通常 250–600 中文字。原标签错误时说明问题，不把错误关系包装成长篇正确结论；需要改旧边在 JSON 外列出建议。

sources 项为 title、url、locator、supports，只填可核查来源，不编造 DOI、页码或链接。未核实的内容明确注明。演示计算说明是假设数值，不冒充实验。

统一符号约定。损伤起始、宏观起裂和裂纹扩展必须区分。公式使用 Obsidian 支持的 $...$ 和 $$...$$。JSON 中换行与反斜杠必须正确转义。返回合法 JSON 代码块；必要的审阅说明放在代码块外。

为避免截断，每批优先补全 2–3 个节点及相关关系；宁可分批完成，不降低正文质量。一个批次可引用已有节点端点，只返回更新的条目。缺失不表示删除。

已有图：<粘贴已有 JSON>
本轮目标：<指定要补全的节点和关系>
```

## 验收

打开节点后能理解公式各项的意义和条件；阅读关系后能解释为何相连；链接可解析；符号一致；人工笔记保留；原始批次不改写；待审阅状态不因正文更长而自动升级。内容更新后重跑全文与结构检查，旧实验脚本不能直接当作 v1.1 导入器。
