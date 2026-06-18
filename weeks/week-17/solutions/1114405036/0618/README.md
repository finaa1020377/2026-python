# 6/18 搜尋效能五階段實驗（1114405036 洪宇）

依 [`../../in_class/0618-search-lab.md`](../../in_class/0618-search-lab.md) 的五階段流程完成。

## Stage 3 — 動手量之前的預測

> 這段在實際量測（`feat: stage3`）之前先寫，作為對照。

- 三種搜尋按「多次查詢」速度，預排序名次猜：binary < bisect << set << builtin_in << linear（越左越快）。
- 交叉點猜：「先排序 + 之後全 binary」大概在**查約 10 次以上**才開始贏過「每次 linear」。

（完整實驗報告於 Stage 5 收尾時補齊。）
