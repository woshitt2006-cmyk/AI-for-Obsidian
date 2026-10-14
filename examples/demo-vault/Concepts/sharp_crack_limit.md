---
kg_id: sharp_crack_limit
kg_type: concept
review_status: pending_human_review
---

# 尖锐裂纹极限

<!-- AIKG:START -->
## 摘要

长度尺度趋于零时相场裂纹表示逼近Griffith尖锐裂纹描述的理论极限。

## 极限在逼近哪一个对象

在适当变分框架中，使 $\ell\to0$ 是让弥散裂纹能量逼近尖锐裂纹能量的理论过程。需要说明完整泛函、函数空间、拓扑、边界条件和其他参数的处理，不能仅看“带宽趋零”就宣布所有结果正确。

## 区分能量、解与演化

用示意记号 $\mathcal E_\ell\xrightarrow{\Gamma}\mathcal E_0$ 表示 Γ-收敛。它包括能量下界与恢复序列等要求；在适当紧性条件下可以研究极小值和极小解的关系。这与固定网格上一次非线性求解的误差不同，也不自动保证所有局部驻点或完整加载路径收敛。

## 双尺度的计算解释

数值中有 $\ell$ 与 $h$。固定 $\ell$ 细化 $h$ 是逼近扩散模型；再考虑 $\ell$ 变小，是另一层模型极限。一个可控的实验设计是对每个 $\ell$ 先检查网格稳定，再比较不同 $\ell$。具体离散收敛条件应取自对应模型与离散方法，不能仅凭保持某个固定比例就宣称完成严格极限。

## 一个容易忽略的区别

尖锐裂纹模型对已有裂纹的传播判据，与无缺陷试样的有限强度预测不是同一个问题。有限尺度相场可能包含强度效应；把 $\ell$ 任意压小可能同时改变这一预测，而不只是让图像更清晰。

## 下一问

你研究的是预裂纹传播、无缺陷起裂还是缺口问题？每类问题需要检验哪些理论与数值条件，才能讨论逼近 Griffith？

## 相关节点与关系详解

- [[Concepts/length_scale_parameter|长度尺度参数]] · `derive` · [[Relations/rel_77ec32a5ab18bbe3|阅读完整关系解释]]（needs_revision）
- [[Concepts/phase_field_fracture|相场断裂]] · `application` · [[Relations/rel_4b60062765279df2|阅读完整关系解释]]（needs_revision）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

