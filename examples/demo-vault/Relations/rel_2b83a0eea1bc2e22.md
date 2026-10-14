# 长度尺度参数 → 有限元离散误差

<!-- AIKG:START -->
关系：`difference` · 状态：`provisional`

[[Concepts/length_scale_parameter|来源节点]] · [[Concepts/finite_element_discretization_error|目标节点]]

## 摘要

长度尺度参数属于连续模型定义，而有限元离散误差来自网格离散，两者影响来源不同。

## 不同来源，不能互相代替

长度尺度是所选连续模型的定义部分；离散误差是该模型连续解与有限自由度近似的差异。两者虽都影响计算输出，却应使用不同实验区分：固定 $\ell$ 细化网格观察数值稳定，再在数值误差可控时比较不同 $\ell$。

例如改变 $\ell$ 导致起裂载荷变化，不能一律称为网格误差；网格足够细也不能替你决定正确材料尺度。这条区别边帮助设计可解释的参数研究。更直接比较 l 与 h 仍可另建边，但不需把本边重复成同义结论。

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

