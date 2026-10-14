# 长度尺度参数 → 相场变量

<!-- AIKG:START -->
关系：`foundation` · 状态：`needs_revision`

[[Concepts/length_scale_parameter|来源节点]] · [[Concepts/phase_field_variable|目标节点]]

## 摘要

长度尺度参数通过梯度项控制相场变量空间变化范围。

## 实际语义是控制剖面

在固定中心的一维 AT2 剖面 $d(x)=e^{-|x|/\ell}$ 中，改变 $\ell$ 改变同一位置的场值与衰减距离。这说明参数通过局部与梯度项的平衡控制空间分布。它没有创造相场变量的定义，也不是理解连续变量的理论基础。

原 foundation 标签仍待调整，建议未来用 controls。完整耦合计算中还会有弹性驱动、边界、约束等影响，所以“由长度尺度控制”也不能被误读为场形态仅由一个参数决定。用这条联系解释带宽时先声明模型与宽度定义。

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

