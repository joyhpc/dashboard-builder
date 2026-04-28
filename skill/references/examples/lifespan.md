# 案例：人口寿命分析仪表盘

**适合场景**：静态（或年度更新）数据，多维分类拆分，主要回答"不同群体怎么比"的问题。比如：人口、收入、教育数据。

## 假设的数据形态

```
列：year, region, gender, age_group, avg_lifespan, mortality_rate, leading_cause, health_spending
```

## 接口设计

- `/api/summary` → `{national_avg, male_avg, female_avg, top_region, bottom_region, yoy_change}`
- `/api/timeline` → 寿命随年份变化，按性别分组（多线折线）
- `/api/distribution` → 主要死因分布（饼）
- `/api/geo` → 各地区寿命（区域地图）
- `/api/factors` → 医疗支出 vs 寿命散点图

## 图表（按重要性排序）

1. **多线折线图** —— 男 vs 女 寿命随时间变化
2. **人口金字塔** —— 年龄 × 性别堆叠条形图（一边用负值技巧）
3. **区域着色地图** —— 各地区寿命
4. **饼图** —— 死因分布
5. **散点图** —— 医疗支出（X）vs 寿命（Y），按地区着色
6. **分组柱状图** —— 男 vs 女 按年龄段对比

## 这个案例独特的地方

- 这种数据集会用到第 5 个接口（`/api/factors`）—— **不要被 3+1 模式束缚**，数据形态需要时就扩展
- **人口金字塔**ECharts 没有原生类型，用两个 bar series（一个 value 取负）共享 Y 轴实现
- 散点图用 `dataset.source` 配合 `encode`，比手动构造 series 干净很多
