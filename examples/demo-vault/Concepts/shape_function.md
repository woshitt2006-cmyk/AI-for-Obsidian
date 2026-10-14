---
kg_id: shape_function
kg_type: concept
review_status: pending_human_review
---

# 形函数

<!-- AIKG:START -->
## 摘要

有限元插值中描述节点值如何影响单元内部场值的基函数。

形函数 $N_i$ 是有限元插值的基础函数。对于节点 i，其满足节点性质：在节点 i 处 $N_i=1$，在其他节点处 $N_i=0$。

形函数定义了单元内部场如何由节点值组合得到：
$$d_h(x)=\sum_iN_i(x)d_i$$

形函数不是任意函数展开，而是有限元近似空间的组成元素。不同单元类型对应不同形函数，例如线性单元使用线性函数，高阶单元使用高阶多项式。

梯度计算依赖形函数梯度：
$$\nabla d_h=\sum_i\nabla N_i d_i$$
因此形函数阶次和网格尺寸共同决定相场梯度的表示能力。

## 审阅说明

节点取值性质适用于这里讨论的节点型 Lagrange 基；不是所有有限元自由度均为点值。未说明分片函数与参考单元。

## 相关节点与关系详解

- [[Concepts/finite_element_interpolation|有限元插值]] · `foundation` · [[Relations/rel_586cdaf8373415de|阅读完整关系解释]]（provisional）

## 来源与核实状态

未提供来源；AI 内容待核实。
<!-- AIKG:END -->

## 我的理解

## 未解决问题

