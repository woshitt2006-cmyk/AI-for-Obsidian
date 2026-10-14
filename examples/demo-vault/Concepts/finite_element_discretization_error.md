---
kg_id: finite_element_discretization_error
kg_type: concept
review_status: pending_human_review
---

# 有限元离散误差

<!-- AIKG:START -->
## 摘要

由网格尺寸有限导致的数值误差，与连续模型中的长度尺度参数不同。

## 误差应相对什么来定义

离散误差比较的是选定连续模型的解与有限元近似。为避免混淆，记固定 $\ell$ 的连续解为 $d_\ell$，网格解为 $d_{\ell,h}$。两者都可能不同于真实材料观测，而后一差异还包含模型误差和参数误差。

## 两个层次的比较

可以考察场范数或实际关注量 $Q$：

$$
e_h=\|d_\ell-d_{\ell,h}\|,\qquad
\delta Q_h=|Q_{\ell,h}-Q_{\ell,h/2}|.
$$

$Q$ 可以是反力、峰值载荷或裂纹能量。相邻网格差异只是收敛诊断，不是没有额外假设就成立的严格误差上界。若没有连续解析解，可以比较多个网格层次并检查稳定趋势。

## 怎样避免把问题归错类

误差还受到单元阶次、网格质量、积分方式与解的光滑性影响。另有非线性迭代误差、载荷步长误差和算法分支选择，不能全部归为有限元离散误差。要检查空间误差，先控制其他误差源，让改变 $h$ 的比较有明确意义。

## 具体诊断与误解

如果固定 $\ell$ 减小 $h$ 后反力曲线稳定，而改变 $\ell$ 后起裂载荷明显变化，第二种变化不能简单叫网格误差。反过来，一条曲线吻合也不证明裂纹路径与局部场准确，多种输出有不同敏感性。

## 下一问

当前科研任务真正关心全局载荷、裂纹位置还是局部梯度？选择不同关注量，所需加密区域与验收容差会怎样变化？

## 相关节点与关系详解

- [[Concepts/length_scale_parameter|长度尺度参数]] · `difference` · [[Relations/rel_2b83a0eea1bc2e22|阅读完整关系解释]]（provisional）
- [[Concepts/finite_element_mesh|有限元网格尺寸]] · `foundation` · [[Relations/rel_cd09588008a3fd47|阅读完整关系解释]]（needs_revision）
- [[Concepts/finite_element_interpolation|有限元插值]] · `foundation` · [[Relations/rel_810389a68c710a00|阅读完整关系解释]]（needs_revision）

## 来源与核实状态

- [An assessment of phase field fracture: crack initiation and growth](https://arxiv.org/html/2103.05443v2)：能量框架、AT 形式及有限元表示；例子和缩放推演是本笔记的教学计算
<!-- AIKG:END -->

## 我的理解

## 未解决问题

