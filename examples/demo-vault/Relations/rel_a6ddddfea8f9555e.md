# 相场断裂 → AT1相场断裂模型

<!-- AIKG:START -->
关系：`extension` · 状态：`provisional`

[[Concepts/phase_field_fracture|来源节点]] · [[Concepts/at1_model|目标节点]]

## 摘要

AT1是变分相场断裂框架中的一种具体模型形式。

## 从通用框架到具体选择

AT1 在共同裂纹密度框架内选择 $w(d)=d$ 与相应归一化常数。它继承位移—损伤能量竞争，同时通过局部代价改变损伤起始。共同框架为 source，具体形式为 target，与当前方向一致。

严格地说“具体形式”更像 specialization 而不是一般 extension；目前标签仍是候选。沿此边阅读时先掌握总能量每一项，再替换局部函数，不必重新理解整套框架。任何阈值推演都要同时给出退化、约束和加载。

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

