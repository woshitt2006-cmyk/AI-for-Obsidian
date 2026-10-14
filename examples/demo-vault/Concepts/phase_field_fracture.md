---
kg_id: phase_field_fracture
kg_type: theory
review_status: pending_human_review
---

# 相场断裂

<!-- AIKG:START -->
## 摘要

利用连续相场变量描述裂纹演化，将尖锐裂纹问题转化为连续场问题。

## 从追踪裂面到求解两个场

尖锐裂纹由几何集合描述，而变分相场断裂用位移 $\mathbf u$ 与连续损伤场 $d$ 描述响应。这里统一采用 $d=0$ 完整、$d=1$ 完全断裂。相场让裂纹分叉和合并通过场分布表现出来，但真实模型仍需要决定能量、边界条件、演化约束与求解方式。

## 一种明确的能量框架

在小应变、准静态、均匀 $G_c$ 的简化脆性模型中，可写

$$
\mathcal E_\ell(\mathbf u,d)=\int_\Omega g(d)\psi_0(\boldsymbol\varepsilon(\mathbf u))\,\mathrm dV
+G_c\int_\Omega\gamma_\ell(d,\nabla d)\,\mathrm dV-\mathcal W_{\mathrm{ext}}.
$$

$\Omega$ 是实体域；$\psi_0$ 是未损伤弹性能密度，单位 J/m³；$g$ 是无量纲退化函数；$\gamma_\ell$ 是裂纹面积密度，单位 1/m；$\mathcal W_{\mathrm{ext}}$ 是外力功。常用 $g(d)=(1-d)^2$，数值实现可能加小残余刚度。张压分裂版本会只退化部分弹性能，不能直接套用此简式预测压缩开裂。

## 机制与求解

降低刚度可能释放弹性能，增加损伤又付出裂纹能量，梯度项反对无限陡的空间变化。求解是在这些竞争下寻找满足边界与不可逆条件的场。损伤不可逆常要求 $d_{n+1}\ge d_n$。交替求位移和损伤容易实施，但联合问题通常非凸；达到数值驻点不保证得到全局最小值。

## 怎样用于当前学习

先问自己“裂纹代价写在哪里”，再检查 $\gamma_\ell$；接着问“宽度由谁决定”，查看 $\ell$；最后问“算得准吗”，固定 $\ell$ 检查网格收敛。AT1/AT2 是同一类框架的不同本构选择，不应仅凭图上一个名称认为所有相场模型完全等价。

## 误解与下一问

相场值不是天然的裂纹开口位移，弥散带宽也不自动等于真实微观过程区宽。需要结合标定解释。下一问：同样的弹性能退化，为什么不同局部裂纹函数会给出不同损伤起始？

## 相关节点与关系详解

- [[Concepts/crack_surface_energy|Griffith裂纹表面能]] · `foundation` · [[Relations/rel_5b2a64d486582151|阅读完整关系解释]]（provisional）
- [[Concepts/ambrosio_tortorelli_regularization|Ambrosio-Tortorelli正则化]] · `foundation` · [[Relations/rel_b542ae6d72fbbef8|阅读完整关系解释]]（provisional）
- [[Concepts/sharp_crack_limit|尖锐裂纹极限]] · `application` · [[Relations/rel_4b60062765279df2|阅读完整关系解释]]（needs_revision）
- [[Concepts/at1_model|AT1相场断裂模型]] · `extension` · [[Relations/rel_a6ddddfea8f9555e|阅读完整关系解释]]（provisional）
- [[Concepts/at2_model|AT2相场断裂模型]] · `extension` · [[Relations/rel_3f39d2ba65887bfb|阅读完整关系解释]]（provisional）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

