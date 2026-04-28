# 案例：项目进度仪表盘

**适合场景**：运营跟踪类数据，每条记录有状态、负责人、截止日期。比如：Jira 工单、销售管线、客服 case、OKR 跟踪。

## 假设的数据形态

```
列：task_id, task_name, owner, status, priority,
    start_date, due_date, completed_date, estimated_hours, actual_hours, module
```

## 接口设计

- `/api/summary` → `{total_tasks, completion_rate, overdue_count, projected_done_date}`
- `/api/timeline` → 燃尽图：剩余任务数随时间变化
- `/api/distribution` → 状态分布（饼或环形）
- `/api/owners` → 每人工作量
- `/api/overdue` → 延期任务列表（表格用）

## 图表（按重要性排序）

1. **燃尽图** —— 剩余开放任务数随时间变化，叠加理想趋势线
2. **环形图** —— 状态分布（待办/进行中/已完成/阻塞）
3. **横向条形图** —— 每人工作量（降序排）
4. **堆叠柱状图** —— 模块名为 X 轴，状态分段堆叠
5. **优先级分布柱状图** —— P0/P1/P2/P3
6. **延期任务表格** —— 不是图表，HTML `<table>` 红色高亮

## 这个案例独特的地方

- **燃尽图的"理想线"** 需要按 start/end 日期算出，不只是画原始数据
- **延期表格**让后端返回 list of dict，前端用小型 JS 表格构建器渲染。**不要硬塞进 ECharts**
- **预计完成日期**需要对完成率做线性回归，`numpy.polyfit` 就够，别用 sklearn
- 这个仪表盘最可能要实时更新——考虑给 `/api/summary` 加 30 秒轮询
