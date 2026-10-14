# Ambrosio-Tortorelli正则化 → 相场断裂

<!-- AIKG:START -->
关系：`foundation` · 状态：`provisional`

[[Concepts/ambrosio_tortorelli_regularization|来源节点]] · [[Concepts/phase_field_fracture|目标节点]]

## 摘要

该正则化理论提供了相场断裂连续裂纹表示的数学基础。

## 从数学近似到计算表示

正则化用局部代价与梯度代价代替尖锐不连续的几何代价。断裂中的相场使用这一结构，使裂纹表示可在固定实体网格上求解。局部项惩罚过广损伤，梯度项惩罚过陡过渡，二者的配合提供了扩散裂纹的空间结构。

这一关系解释了梯度为何出现在能量中，但不独自给出材料本构、加载策略或损伤不可逆性。AT 的原始自由不连续问题与机械断裂之间需要明确转接；有相似正则化结构，也不意味着所有动力学断裂问题都满足同一极限结论。

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

