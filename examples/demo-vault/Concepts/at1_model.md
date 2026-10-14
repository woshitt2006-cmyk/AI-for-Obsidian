---
kg_id: at1_model
kg_type: theory
review_status: pending_human_review
---

# AT1相场断裂模型

<!-- AIKG:START -->
## 摘要

采用线性裂纹密度函数的变分相场断裂模型，具有损伤起始阈值。

## AT1 的具体选择

采用 $d=0$ 完整、$d=1$ 断裂，在常用的同一归一化下，AT1 取 $w(d)=d$，$c_w=2/3$。这里“线性”只指局部裂纹函数，整个能量还含梯度项和弹性退化，并非线性问题。

$$
\gamma_\ell^{\mathrm{AT1}}=\frac{3}{8}\left(\frac d\ell+\ell|\nabla d|^2\right).
$$

## 用一维均匀例子理解起始阈值

为说明机制，设小应变单轴拉伸、均匀 $d$、$g(d)=(1-d)^2$、$\psi_0=E\varepsilon^2/2$，省略外力势并考虑初始状态 $d=0$。能量密度对损伤的右导数为

$$
\left.\frac{\partial\psi}{\partial d}\right|_{d=0}=-2\psi_0+\frac{3G_c}{8\ell}.
$$

在 $0\le d$ 约束下，右导数为正时初始损伤没有降低能量的驱动力；阈值对应 $\psi_0=3G_c/(16\ell)$。教学推演显示有限的无损伤弹性阶段从何而来。$E$ 是杨氏模量，$\varepsilon$ 是应变；梯度为零的例子不能代表缺口附近的复杂场。

## 如何比较而不混淆

损伤刚开始变化、结构达到峰值以及可观察裂纹形成，需要分别定义。阈值结论依赖此处的局部函数、退化函数与约束；换一个模型不能照搬。与 AT2 比较时先固定这些共同选择，才能把差异归于 $w$。

## 下一问

引入缺口、梯度和张压分裂后，均匀材料点的阈值如何转化为结构层面的起裂预测？

## 相关节点与关系详解

- [[Concepts/phase_field_fracture|相场断裂]] · `extension` · [[Relations/rel_a6ddddfea8f9555e|阅读完整关系解释]]（provisional）
- [[Concepts/at2_model|AT2相场断裂模型]] · `difference` · [[Relations/rel_83d1baef5f0114ae|阅读完整关系解释]]（provisional）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

