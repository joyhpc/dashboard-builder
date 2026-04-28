# 案例：恶劣天气仪表盘

**适合场景**：实时或时序数据，带严重等级，跨多个地点。比如：天气预警、IoT 传感器读数、事件日志、监控告警。

## 假设的数据形态

```
列：date, region, weather_type, alert_level, temperature, precipitation, wind_speed, duration_hours
```

## 接口设计

- `/api/summary` → `{active_alerts, max_temp, min_temp, regions_affected, longest_alert}`
- `/api/timeline` → 温度 + 降水量随时间变化（双 Y 轴）
- `/api/distribution` → 天气类型分布
- `/api/geo` → 各地区预警等级（区域着色地图）

## 图表（按重要性排序）

1. **双 Y 轴折线图** —— 温度（左轴）+ 降水量（右轴），首屏顶部
2. **区域着色地图** —— 预警等级红/橙/黄
3. **饼图** —— 天气类型分布
4. **柱状图** —— 各地区预警数量（可排序）

## 这个案例独特的地方

- **颜色编码很重要**：红色=严重、橙色=警告、黄色=提示。要覆盖默认调色板
- **时间趋势必须双 Y 轴**：温度（℃）和降水量（mm）量级差太大，单 Y 轴会让其中一个看不清
- **如果实时更新**：前端加 `setInterval(fetchAndUpdate, 60000)` 每分钟刷新，不要依赖手动 F5
