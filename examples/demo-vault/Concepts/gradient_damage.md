---
kg_id: gradient_damage
kg_type: theory
review_status: pending_human_review
---

# 梯度损伤模型

<!-- AIKG:START -->
## 摘要

通过损伤梯度描述材料内部长度尺度效应的一类模型。

## 为什么局部损伤会遇到空间问题

损伤本构让材料逐渐软化。如果软化完全局部，变形可能集中到依赖网格的一条极窄带，耗散也会受离散影响。梯度增强或非局部模型通过空间耦合引入特征长度；不同模型的变量和方程并不完全相同。

## 一个示意模型

以隐式梯度平均为例，可写

$$
\bar\varepsilon-L^2\Delta\bar\varepsilon=\tilde\varepsilon.
$$

$\tilde\varepsilon$ 是局部等效应变，$\bar\varepsilon$ 是用于损伤驱动的平滑量，均无量纲；$L$ 是平均作用长度，$\Delta$ 是拉普拉斯算子。还需要边界条件和损伤演化律才能形成完整模型。此式仅代表一类隐式梯度方法，不等同于所有梯度损伤的定义。

## 直觉与相场联系

单个点的响应会受周围区域影响，因而局部软化不再完全脱离邻域。相场断裂也包含梯度耦合，二者有相似的微分结构；不过变量、驱动力、退化律、能量校准和损伤区演化可能不同。不能看到一个 $L^2\Delta$ 项，就认定两个模型参数可以直接互换。

## 当前关系的修正理由

图中“梯度损伤模型 ↔ 长度尺度参数”把一个模型族与一个参数作类比，层级不一致。更合适的是比较模型族，或者另外建立“梯度损伤内部长度”节点再比较尺度。原边仍标记待调整，其解释只能作为探索线索。

## 如何使用与下一问

比较两个模型时列出被平滑的变量、损伤驱动力、边界条件和耗散标定，而不是只看公式外形。下一问：在相同单轴试验标定后，两个模型的损伤带宽是否仍可能不同？

## 相关节点与关系详解

- [[Concepts/length_scale_parameter|长度尺度参数]] · `analogy` · [[Relations/rel_5c6fddaa973c8ef2|阅读完整关系解释]]（needs_revision）

## 来源与核实状态

- [Gradient damage vs phase-field approaches for fracture: similarities and differences](https://eprints.whiterose.ac.uk/id/eprint/100669/1/gradient-phase_revision.pdf)：梯度损伤与相场的结构联系及区别
<!-- AIKG:END -->

## 我的理解

## 未解决问题

