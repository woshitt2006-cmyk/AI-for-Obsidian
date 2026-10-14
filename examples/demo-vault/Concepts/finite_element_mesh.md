---
kg_id: finite_element_mesh
kg_type: concept
review_status: pending_human_review
---

# 有限元网格尺寸

<!-- AIKG:START -->
## 摘要

有限元离散中单元空间尺度，影响连续场和梯度的解析能力。

## 网格尺寸是求解分辨率

有限元用有限自由度近似连续场，$h$ 表示某个单元的特征尺寸。在非均匀网格中 $h$ 是局部量，不应只报告全局平均值。对相场计算，重点是潜在裂纹带附近的单元尺寸、阶次、形状与方向。

## 插值与局部变化

相场离散可写

$$
d_h(\mathbf x)=\sum_iN_i(\mathbf x)d_i,\qquad
\nabla d_h=\sum_i\nabla N_i(\mathbf x)d_i.
$$

$N_i$ 是单元形函数，$d_i$ 是节点相场值。每个单元内可表示的变化由形函数决定。若过渡带内只有极少单元，场值和梯度可能都被解析得很差，而裂纹能量恰好依赖二者。

## 为什么比较 $h/\ell$

比值 $h/\ell$ 无量纲，是比较离散尺度与模型尺度的方便量。它小一些通常有利于解析过渡层，但充分精度取决于单元、几何、模型与关注的输出。不能对所有问题规定一个通用比例。提高阶次或局部加密也会改变精度与成本。

## 一个验证实验

固定材料、$\ell$、加载、求解容差与单元类型，只改变裂纹区 $h$，比较反力、耗散能、峰值载荷及路径。若这些观测仍显著改变，说明结果尚不能被视为对该连续模型的稳定近似。如果同时改 $\ell$，就把离散和模型变化混在一起。

## 常见误解与下一问

“已经使用非局部模型”不意味着任意粗网格都准确；细网格也不能自动修正错误本构或不收敛的非线性求解。下一问：我需要哪些输出同时稳定，才能说当前问题达到了所需网格精度？

## 本次追问补充：插值与分辨率

有限元网格尺寸 h 描述离散单元的空间大小。它不是相场模型中的长度尺度 l。

固定 l 时减小 h，是在更准确地求解同一个正则化相场问题；而减小 l 并同步减小 h，则是在改变连续模型，使裂纹过渡区域趋近尖锐裂纹。

网格需要能够解析长度尺度控制的相场变化，因为裂纹能量包含梯度项，例如 $|\nabla d|^2$。如果过渡区域只覆盖很少单元，有限元插值可能无法准确表示相场和梯度。

## 相关节点与关系详解

- [[Concepts/length_scale_parameter|长度尺度参数]] · `prerequisite` · [[Relations/rel_35d20c4c4d22f693|阅读完整关系解释]]（provisional）
- [[Concepts/finite_element_discretization_error|有限元离散误差]] · `foundation` · [[Relations/rel_cd09588008a3fd47|阅读完整关系解释]]（needs_revision）
- [[Concepts/finite_element_interpolation|有限元插值]] · `foundation` · [[Relations/rel_c061c4633191de34|阅读完整关系解释]]（needs_revision）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

