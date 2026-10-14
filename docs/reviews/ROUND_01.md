# 第一轮 JSON 审阅

## 结构结果

输入为合法的 v1 数据结构：7 个节点、6 条边；ID 唯一，节点与关系类型在允许范围内，端点存在，无自环。节点覆盖基础理论、连续表示、长度尺度和数值离散，适合用作第一轮候选图。

此检查不代表物理内容已全部核实，也不代表第一轮学习验收已经完成。

## 逐条关系判断

| 关系 | 初步判断 | 后续处理 |
| --- | --- | --- |
| Griffith裂纹表面能 → 相场断裂：foundation | 对 Griffith 型变分相场框架合理 | 在描述中明确“Griffith 型脆性变分相场”，避免泛指全部相场模型 |
| AT正则化 → 相场断裂：foundation | 对相关变分模型合理 | 明确历史来源与模型范围，不把它写成所有相场断裂的唯一基础 |
| 长度尺度 → 相场变量：foundation | 物理联系合理，关系标签不准确 | 它表达控制空间分布的作用，不是理论基础；暂标待调整 |
| AT正则化 → 长度尺度：derive | 可理解为正则化形式引入参数 | “引入”不等于通过推导确定其数值；描述应明确参数值仍需选择或标定 |
| 长度尺度 → 网格尺寸：prerequisite | 在“理解网格选择”的教学语义下可保留 | 明确不是 l 推导出唯一 h；网格分辨率需结合模型、单元与收敛检查 |
| 梯度损伤模型 ↔ 长度尺度：analogy | 对象层级不一致 | 建议比较“梯度损伤模型 ↔ 相场断裂”，或增加“梯度损伤内部长度”节点再比较两个尺度 |

这里的关系标签判断是对本项目协议的设计审阅，而非文献给出的分类。

## 节点表述建议

- phase_field_fracture：theory 可以保留；此前设计示例中的 method 不是固定分类要求。本实验统一保留用户选择，跨轮次保持一致。
- crack_surface_energy：目前 description 没有公式，equation 类型可用但内容不足。后续在明确假设后补公式，或改为 concept；不能仅因名称自行填入公式。
- phase_field_variable：补充 d 的完整/断裂端点约定，避免不同资料中的相反定义造成混淆。
- length_scale_parameter：建议改为“控制扩散裂纹的特征宽度；在 Griffith 型变分正则化中承担正则化作用，有限取值也可能影响起裂等预测，解释取决于模型与标定。”
- ambrosio_tortorelli_regularization：建议注明它对 Mumford–Shah 类泛函的近似启发了相应变分断裂正则化，不把原始理论直接等同于所有断裂模型。

## 协议暴露的问题

当前七种关系缺少“参数控制”这一类。第一轮暂不扩充枚举，以免直接破坏 v1 兼容性；保留原边并标记 needs_revision。待三轮结束后，判断这种关系是否频繁出现，再决定 v1.1 是否加入 controls。不要为了通过校验强行用 foundation 表达全部联系。

示例 graph.json 增加 review_status 作为本地状态元数据，它不属于发送给 ChatGPT 的原始 v1 协议。original.json 保留提交内容。图谱包含候选边，用于审阅；尚无经用户确认的正式关系集合。

## 第二轮建议

问题：**长度尺度 l 与网格尺寸 h 为什么必须区分？固定 l 时细化网格，与减小 l 并同步细化网格，分别在改变什么？**

这是一个可比较的探索分支：它连接现有正则化与离散节点，能够检验相同术语是否被混用。提示词已保存于示例 Vault 的 _AIKG/prompts/round_02.txt。

第一轮仍需用户填写：最有帮助的连接、用自己的话解释一条关系、从图中产生的下一问。仅凭 JSON 无法代替这些学习反馈。

## 查阅来源

[Kristensen、Niordson 与 Martínez-Pañeda：An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/abs/2103.05443) 讨论 Griffith 框架、模型选择与内部材料长度对预测的作用，支持对长度尺度表述加上模型限定；并不逐条认证本图。

[Mesh refinement procedures for the phase field approach to brittle fracture](https://www.sciencedirect.com/science/article/pii/S0045782521005454) 的检索摘要涉及网格解析扩散裂纹的要求；本次全文页面访问受限，因此没有据此指定数值阈值。具体比例留待第二轮凭可访问的全文核查。

## 交付与验证

KnowledgeVault_Demo 包含 7 篇节点笔记、主题 Canvas、原始 JSON、本地候选图和第二轮提示词。脚本检查了 ID、枚举、端点和 Canvas 文件引用。尚未在真实 Obsidian 界面打开验收。
