---
kg_id: ambrosio_tortorelli_regularization
kg_type: theory
review_status: pending_human_review
---

# Ambrosio-Tortorelli正则化

<!-- AIKG:START -->
## 摘要

将尖锐裂纹能量泛函转化为含梯度项的连续形式。

## 正则化解决哪种困难

原始 Ambrosio–Tortorelli 思路来自对 Mumford–Shah 类自由不连续泛函的近似。它启发了将尖锐裂纹能量改写为连续场能量的变分断裂方法。这里讨论其在断裂中的使用，而不是声称原理论从一开始就是断裂本构模型。

## 尖锐面到连续场

计算上的难点是未知集合 $\Gamma$。一种 AT2 风格的近似是

$$
G_c\int_\Gamma\mathrm dA\quad\leadsto\quad
G_c\int_\Omega\left(\frac{d^2}{2\ell}+\frac{\ell}{2}|\nabla d|^2\right)\mathrm dV.
$$

符号 $\leadsto$ 表示构造近似，不是有限 $\ell$ 时逐点相等。$d$ 是无量纲场，$\ell$ 提供长度，体积分才能得到 J。配合弹性退化与合适的残余刚度等参数极限，构造完整近似泛函还需要相应假设。

## 为什么梯度项不能省

若只保留局部项，损伤可以收缩到极窄区域以降低能量，却不付出空间变化的代价；如果只有梯度项，则又缺少对广泛损伤的局部惩罚。由两个代价的竞争得到有结构的过渡层。归一化选择的目标之一是让一个理想裂纹剖面支付合适的单位面积能量。

## 参数不是被算出来的常数

这套结构引入 $\ell$，但没有仅靠正则化理论就给定某种材料必须取多少毫米。极限结论与有限参数标定是两个层次。AT1 同属常用的变分梯度损伤/相场族，但其局部函数与经典二次形式不同，引用原始 AT 理论时要避免省略这些区别。

## 下一问

一个近似泛函具有什么收敛意义？为何能量收敛仍不足以保证任意求解算法给出的演化路径准确？

## 相关节点与关系详解

- [[Concepts/phase_field_fracture|相场断裂]] · `foundation` · [[Relations/rel_b542ae6d72fbbef8|阅读完整关系解释]]（provisional）
- [[Concepts/length_scale_parameter|长度尺度参数]] · `derive` · [[Relations/rel_6036d00650995445|阅读完整关系解释]]（provisional）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

