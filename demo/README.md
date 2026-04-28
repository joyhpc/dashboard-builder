# 🌡️ Demo：全球城市气温仪表盘

这是 dashboard-builder skill 的**完整示例项目**。下载下来 `pip install` 然后 `python app.py`，就能在浏览器看到一个跑起来的仪表盘——5 张图、12 座城市、10 年数据。

## 它长什么样

> 跑起来后用浏览器截图替换这里。位置：`screenshots/dashboard.png`

包含：
- **5 个 KPI 卡片**：覆盖城市、数据记录、最高温、最低温、十年升温
- **月平均气温趋势图**（含 12 个月移动平均，能看到清晰的升温趋势）
- **2023 年各城市年均温横向条形图**（颜色按温度梯度变化）
- **天气类型环形图**（晴 / 多云 / 雨 / 雾 占比）
- **城市地理散点图**（经纬度坐标 + 温度色标）

## 快速运行

```bash
# 1. 进入 demo 目录
cd demo

# 2. 安装依赖（只需要 flask 和 pandas）
pip install -r requirements.txt

# 3. 启动
python app.py
```

然后浏览器打开 **http://localhost:5000** 即可。

按 `Ctrl+C` 停止服务。

## 数据说明

`data.csv` 是基于真实城市气候特征**合成的演示数据**（不是真实历史观测）：

- 12 个城市覆盖 5 大洲、北半球与南半球
- 时间范围 2014-01-01 到 2023-12-31，日度数据
- 用真实年均温作基线，叠加季节性正弦波动 + 真实的全球升温趋势（约 0.04℃/年）+ 随机噪声
- 总计约 4.4 万条记录，~2.5 MB

如果想重新生成数据（比如改时间范围、改城市列表），编辑 `generate_data.py` 顶部的 `CITIES`、`START_DATE`、`END_DATE` 然后：

```bash
python generate_data.py
```

为什么用合成数据而不是真实数据？
1. 仓库自包含、不依赖外部 API、没有版权风险
2. 真实数据集动辄几百 MB，不适合 demo
3. 合成数据的趋势是已知的，演示效果稳定

## 文件结构

```
demo/
├── app.py                 # Flask 后端（5 个 API 接口）
├── data.csv               # 数据文件
├── generate_data.py       # 数据生成脚本（可选）
├── requirements.txt       # Python 依赖
├── templates/
│   └── index.html         # 前端页面（HTML + ECharts）
└── screenshots/           # 跑起来的截图
```

## 想改成自己的数据？

这正是 dashboard-builder skill 要解决的问题。回到仓库根目录，看 [INSTALL.md](../INSTALL.md) 把 skill 装进 Claude，然后跟 Claude 说"帮我用我的 xxx 数据做一个仪表盘"，它会自动按这个 demo 的模式生成你自己的版本。
