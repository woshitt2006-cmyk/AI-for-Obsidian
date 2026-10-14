# 梯度损伤模型 → 长度尺度参数

<!-- AIKG:START -->
关系：`analogy` · 状态：`needs_revision`

[[Concepts/gradient_damage|来源节点]] · [[Concepts/length_scale_parameter|目标节点]]

## 摘要

梯度损伤模型中也存在内部长度尺度，但其物理解释可能不同于经典相场断裂中的正则化尺度。

## 类比应比较同层级对象

梯度损伤的内部长度与相场中的长度尺度都参与空间耦合，但其变量、驱动力和标定目的可能不同。这提供了一条研究线索，而原边把模型族直接与参数比较，语义不完整。

建议改为比较梯度损伤与相场模型，或者先建立内部长度节点。相似的拉普拉斯结构不保证等价的耗散、过程区或边界效应；未验证映射时不能把一种模型标定的长度直接代入另一种。本边保持待调整，关系正文用于说明修改理由。

## 来源与核实状态

- [Gradient damage vs phase-field approaches for fracture: similarities and differences](https://eprints.whiterose.ac.uk/id/eprint/100669/1/gradient-phase_revision.pdf)：梯度损伤与相场的结构联系及区别
<!-- AIKG:END -->

## 我的理解

## 未解决问题

