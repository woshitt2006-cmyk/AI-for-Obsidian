---
kg_id: length_scale_parameter
kg_type: concept
review_status: pending_human_review
---

# 长度尺度参数

<!-- AIKG:START -->
## 摘要

控制裂纹正则化区域宽度的参数l，在经典相场断裂中主要是数学正则化尺度。

## 一个参数的两个问题

长度尺度 $\ell>0$ 有长度单位，控制扩散裂纹的特征变化距离。必须分别问：它在理论近似中做什么，以及在有限取值的具体模型中改变什么。前者涉及尖锐裂纹极限，后者可能涉及有限强度和标定，不能简单把所有情况称为纯数值参数。

## 为什么同时出现 $1/\ell$ 和 $\ell$

一般裂纹密度常写成

$$
\gamma_\ell=\frac{1}{4c_w}\left(\frac{w(d)}{\ell}+\ell|\nabla d|^2\right),\qquad c_w=\int_0^1\sqrt{w(s)}\,\mathrm ds.
$$

$w$ 是无量纲局部损伤代价，$c_w$ 是归一化常数。两项都具有 1/m 单位。局部项反对广泛损伤，梯度项反对过陡变化；两者竞争才产生有限宽度。

## 用缩放理解宽度

假设一维剖面在宽度 $b$ 内变化，粗略取 $d=O(1)$、$|d'|=O(1/b)$。裂纹能量尺度为 $G_c(b/\ell+\ell/b)$，省略系数。宽度太大会抬高局部项，太小会抬高梯度项，平衡给出 $b=O(\ell)$。这是量纲缩放推演，不是精确宽度公式。

## 有限尺度与网格

一些标准 AT 模型的均匀强度具有 $\sigma_c\propto\sqrt{EG_c/\ell}$ 的尺度关系；比例系数与模型、加载和假设有关。减小 $\ell$ 不仅让带变窄，也可能改变起裂预测。网格尺寸 $h$ 是离散尺度，减小它是在更精细地求解已经选定的连续模型。固定 $\ell$ 细化 $h$ 与改变 $\ell$ 不是同一种实验。

## 选参和下一问

记录 $\ell$ 的选择依据：近似参数还是根据强度、过程区信息标定？在同一 $\ell$ 下检查力—位移、能量和裂纹路径的网格敏感性，再评估换 $\ell$ 的模型敏感性。不要用一次粗网格结果反推材料尺度。下一问：哪些观测足以区分模型尺度变化与离散误差？

## 相关节点与关系详解

- [[Concepts/phase_field_variable|相场变量]] · `foundation` · [[Relations/rel_e02a62f93f0b8bf8|阅读完整关系解释]]（needs_revision）
- [[Concepts/ambrosio_tortorelli_regularization|Ambrosio-Tortorelli正则化]] · `derive` · [[Relations/rel_6036d00650995445|阅读完整关系解释]]（provisional）
- [[Concepts/finite_element_mesh|有限元网格尺寸]] · `prerequisite` · [[Relations/rel_35d20c4c4d22f693|阅读完整关系解释]]（provisional）
- [[Concepts/gradient_damage|梯度损伤模型]] · `analogy` · [[Relations/rel_5c6fddaa973c8ef2|阅读完整关系解释]]（needs_revision）
- [[Concepts/finite_element_discretization_error|有限元离散误差]] · `difference` · [[Relations/rel_2b83a0eea1bc2e22|阅读完整关系解释]]（provisional）
- [[Concepts/sharp_crack_limit|尖锐裂纹极限]] · `derive` · [[Relations/rel_77ec32a5ab18bbe3|阅读完整关系解释]]（needs_revision）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

