---
kg_id: finite_element_interpolation
kg_type: method
review_status: pending_human_review
---

# 有限元插值

<!-- AIKG:START -->
## 摘要

利用节点自由度和形函数构造连续场近似的方法。

有限元不能直接表示连续函数 d(x)，而是在有限维函数空间中寻找近似解。对于有限元空间 V_h，近似场写为 $d_h(x)=\sum_iN_i(x)d_i$。其中 $d_i$ 是节点自由度，$N_i$ 是形函数。

该公式不是任意连续函数的恒等展开，而是有限元选定近似空间中的表示。真实相场 $d(x)$ 与离散相场 $d_h(x)$ 一般不同，误差来自有限维空间无法完全包含真实解。

求梯度时：
$$\nabla d_h=\sum_i\nabla N_i d_i$$
因为节点值 $d_i$ 是固定未知量，不随单元内部坐标变化，空间变化完全由形函数决定。

一维两节点线性单元中，若节点坐标为 $x_1=0,x_2=L$，形函数为 $N_1=(L-x)/L,N_2=x/L$。若节点值为 $d_1,d_2$，则：
$$d_h=N_1d_1+N_2d_2$$
梯度为：
$$\frac{dd_h}{dx}=\frac{d_2-d_1}{L}$$
说明有限元只能按照选定函数形式描述节点之间的变化。

在相场断裂中，如果裂纹区域宽度由长度尺度 l 控制，而网格尺寸 h 太大，则有限元空间无法准确描述 d 的快速变化，也无法准确计算 $|\nabla d|^2$。

常见误解：细化网格 h 不等于改变长度尺度 l。h 改变的是离散精度，l 改变的是连续模型。

## 审阅说明

任意连续场不能被有限空间精确表示，但属于该空间的连续函数可以；节点系数求解前未知，空间求导时是常数。缺少具体数值例子与参考坐标映射。

## 相关节点与关系详解

- [[Concepts/shape_function|形函数]] · `foundation` · [[Relations/rel_586cdaf8373415de|阅读完整关系解释]]（provisional）
- [[Concepts/finite_element_mesh|有限元网格尺寸]] · `foundation` · [[Relations/rel_c061c4633191de34|阅读完整关系解释]]（needs_revision）
- [[Concepts/finite_element_discretization_error|有限元离散误差]] · `foundation` · [[Relations/rel_810389a68c710a00|阅读完整关系解释]]（needs_revision）

## 来源与核实状态

未提供来源；AI 内容待核实。
<!-- AIKG:END -->

## 我的理解

## 未解决问题

