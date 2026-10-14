# 相场断裂 → AT2相场断裂模型

<!-- AIKG:START -->
关系：`extension` · 状态：`provisional`

[[Concepts/phase_field_fracture|来源节点]] · [[Concepts/at2_model|目标节点]]

## 摘要

AT2是变分相场断裂框架中的一种具体模型形式。

## 同一框架中的另一种局部代价

AT2 取 $w(d)=d^2$，归一化后有 $d^2/(2\ell)+\ell|\nabla d|^2/2$。它同样继承场耦合和能量竞争，但初始点局部裂纹代价的导数不同，进而改变损伤起始。

方向由共同框架指向具体形式，语义上仍更适合 specialization。相同框架不保证相同材料参数能给出相同起裂预测。该边帮助把“框架共享”与“本构不同”区分开，并引向与 AT1 的受控比较。

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

