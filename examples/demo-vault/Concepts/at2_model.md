---
kg_id: at2_model
kg_type: theory
review_status: pending_human_review
---

# AT2相场断裂模型

<!-- AIKG:START -->
## 摘要

采用二次裂纹密度函数的变分相场断裂模型，损伤演化更加弥散。

## AT2 的具体选择

在同样的损伤约定下，AT2 取 $w(d)=d^2$，$c_w=1/2$，于是

$$
\gamma_\ell^{\mathrm{AT2}}=\frac{d^2}{2\ell}+\frac\ell2|\nabla d|^2.
$$

二次项只描述局部裂纹代价，完整求解仍耦合位移与损伤。不要只用“更加弥散”替代具体本构解释，因为场宽还与加载和边界有关。

## 为什么没有同样的正起始阈值

在均匀一维教学例子中，$g(d)=(1-d)^2$、$\psi_0=E\varepsilon^2/2$。在 $d=0$，能量密度右导数为 $-2\psi_0$，只要弹性能为正，就有初始损伤驱动力。由均匀驻值条件可解得

$$
d=\frac{2\psi_0}{2\psi_0+G_c/\ell}.
$$

这表示小载荷下也可能出现小损伤；不表示结构一施加载荷就出现宏观裂缝或丧失承载力。忽略梯度、约束激活与历史效应的这个例子只用来说明局部机制，不能当作一般演化解。

## 怎样解释计算曲线

随着损伤增加，退化降低应力，但仍可能存在有限峰值。相比 AT1 的初始无损伤阶段，AT2 在此标准例子中会更早偏离未损伤响应。若把数值中某个 $d$ 阈值定义为“起裂”，报告时必须说明阈值，否则无法比较不同模型的起裂载荷。

## 下一问

同一 $G_c$ 和 $\ell$ 下，AT1/AT2 为什么不必具有相同峰值强度？是否应按同一材料强度分别标定尺度后再比较？

## 相关节点与关系详解

- [[Concepts/phase_field_fracture|相场断裂]] · `extension` · [[Relations/rel_3f39d2ba65887bfb|阅读完整关系解释]]（provisional）
- [[Concepts/at1_model|AT1相场断裂模型]] · `difference` · [[Relations/rel_83d1baef5f0114ae|阅读完整关系解释]]（provisional）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

