---
name: dashboard-builder
description: 根据用户提供的数据集（Excel、CSV、API 或数据库）快速生成一个完整可部署的 Flask + ECharts 数据可视化仪表盘项目。当用户提到"做一个仪表盘"、"数据可视化"、"看板"、"dashboard"、"BI 页面"、"数据监控页"，或者拿着表格数据问"怎么把这些数据用图表展示在网页上"时，请使用此技能——即使用户没有明确说"仪表盘"三个字。产出的项目结构固定为：Flask 后端提供 3-4 个 JSON API、单页 HTML 前端展示 KPI 卡片和 ECharts 图表、附带 requirements.txt。不适用：单张静态图表（用 matplotlib 即可）、纯前端组件（不涉及数据后端）、Tableau/PowerBI 等第三方 BI 工具配置。
---

# Dashboard Builder

把"数据集 → 可在浏览器打开的仪表盘"这条路径标准化成 5 步流程。每次生成的项目结构相同：Flask 后端 + 单页 HTML 前端 + ECharts 图表 + requirements.txt。

## 我应该读哪些文件？

本文件是路由地图。代码模板和案例分别在不同子目录，**用到时再读**——不要一次性全部读完。

| 你正在做的事 | 应该读 |
|---|---|
| 走完整 5 步流程 | 本文件（你已经在这儿） |
| 选图表类型不确定 | §4 决策树 |
| 写 Flask 后端 | `assets/backend/app_template.py` |
| 写 HTML 前端 | `assets/frontend/index_template.html` |
| 找类似场景的参考案例 | `references/examples/` 里挑最像的一个 |
| 用户问部署、nginx、gunicorn | `references/deployment.md` |
| 用户报错了 | `references/troubleshooting.md` |

---

## Step 0：先判断要不要问用户

动手前先看信息够不够：

- **够了** = 用户上传了数据文件 + 说清楚关心什么指标 + 大致提到想要什么图。直接跳到 Step 1。
- **不够** = 数据源、核心指标、图表偏好这三项里有任何一项模糊。**用 `ask_user_input_v0` 工具**给按钮选项，最多问 3 个问题：
  1. 数据从哪来？（Excel / CSV / API / 数据库）
  2. 主要想看什么？（时间趋势 / 分类对比 / 地理分布 / 综合）
  3. 数据多久更新？（一次性静态 / 每天刷新 / 实时）

不要一次性追问所有细节。先用合理默认值开干，跑通后再迭代。

## Step 1：实地查看数据

如果用户上传了文件，**先 `pd.read_excel/read_csv` 读一下前几行**，再设计任何东西。不要假设字段名或类型。

读完用一句话向用户确认你看到的字段：「我看到数据有这些列：日期、城市、温度。我会按这个理解来做，对吗？」

如果用户只是描述了数据没给文件，列出你假设的字段让他确认。

## Step 2：设计数据模型（3+1 接口模式）

> **3+1 接口模式 = 一个总览接口 + 三个分主题接口**。每次都按这个套路设计后端，省得每次重新发明轮子。

每个仪表盘都暴露这套接口形状，按需挑选：

| 接口路径 | 返回内容 | 是否必需 |
|---|---|---|
| `/api/summary` | KPI 卡片数据：总数、最大值、最小值、平均值、最后更新时间 | **必需** |
| `/api/timeline` | 时间序列：`{dates: [...], values: [...], moving_avg?: [...]}` | 数据有日期列就要 |
| `/api/distribution` | 分类分布：`{categories: [...], values: [...], percentages: [...]}` | 数据有分类列就要 |
| `/api/geo` | 地理数据：`{regions: [...], values: [...]}` 或 `{cities: [{name, lat, lon, value}]}` | 数据有地点列就要 |

不需要四个全做。人口数据可能只需要 summary + distribution + geo。项目跟踪可能用 summary + timeline + distribution。看数据形状决定。

## Step 3：搭后端

复制 `assets/backend/app_template.py` 和 `requirements.txt` 到输出目录，然后：

1. 改 `load_data()` 函数对接用户实际的数据源
2. 实现你在 Step 2 选定的那几个 `prepare_*_data()` 函数——这是**唯一真正定制的部分**，路由骨架原样复用
3. 确认 `prepare_summary_data()` 返回的字段名跟前端 KPI 卡片用的 `id` 一一对应

**最容易踩的坑**：数据有日期列时，必须先 `pd.to_datetime()` 转换才能按时间分组。返回 JSON 前要把 Timestamp 转成字符串（用 `.dt.strftime('%Y-%m-%d')`），否则 jsonify 会抛错。

## Step 4：选图表（决策树）

> Claude 容易"想象力过剩"乱推荐花哨图表。严格按下面这棵树走，按"用户想回答什么问题"选图，不是按"数据是什么类型"。

```
用户想回答的问题是？

├─ 「X 随时间怎么变？」              → 折线图（单线 / 多线）
│   └─ 两个指标量级差很大？           → 双 Y 轴折线图
│
├─ 「不同类别怎么比？」
│   ├─ 类别 ≤ 10 个                   → 竖向柱状图
│   ├─ 类别 > 10 个                   → 横向条形图（标签有空间）
│   └─ 多维度对比                     → 分组柱状图
│
├─ 「占比 / 份额是？」
│   ├─ 2-5 块                         → 饼图
│   ├─ 6+ 块                          → 环形图 + 图例 / 树状图
│   └─ 有层级关系                     → 旭日图
│
├─ 「在哪里发生？」                   → 地图（区域用 choropleth，散点用气泡图）
│
└─ 「什么流向什么？」                 → 桑基图 / 力导向图
```

> **术语补充**：choropleth = 区域着色地图，颜色深浅代表数值大小（比如各省 GDP 颜色深浅图）；气泡图 = 散点图但点的大小代表第三个维度。

**一个问题对应一张图**。8 个图回答 8 个不同问题是好仪表盘；8 个图回答同一个问题的 8 种角度是冗余。

## Step 5：搭前端

复制 `assets/frontend/index_template.html`。对每个 Step 4 选定的图：

1. 加一段 `<div class="chart-wrapper"><div class="chart" id="my-chart"></div></div>` 到布局里
2. 加一个对应的 `initMyChart(data)` 函数（克隆模板里 `initTimelineChart` 的写法）
3. 把它加到顶部的 `Promise.all([...])` 加载链里

模板用了：ECharts CDN（`echarts.min.js`）、深色主题（背景 `#0f1c3a`）、CSS Grid 自适应布局。**不要重新发明**。除非用户要求改主题色，否则保持原样。

## 输出位置

最终交付始终长这样。文件创建在 `/mnt/user-data/outputs/<项目名>/`，方便用 `present_files` 工具让用户下载：

```
<项目名>/
├── app.py
├── data.xlsx              （或用户上传的任何数据文件，复制进来）
├── templates/
│   └── index.html
├── requirements.txt
└── README.md              （一段话：怎么装、怎么跑）
```

README 必须包含两条命令：`pip install -r requirements.txt` 和 `python app.py`，告诉用户默认端口 5000，浏览器打开 `http://localhost:5000`。

## 交付完成后

最多提一个具体的后续建议（不要列两个都说）：

- 「要不要加一个[具体图]来回答[具体问题]？」——提具体的、跟数据相关的，不要泛泛问「还要加图吗」
- 「要不要部署上线？我可以加 gunicorn + nginx 配置。」——只在用户透露出生产部署意图时说

不要问「还有别的问题吗？」这种废话。要么提具体建议，要么就停。

---

## 必须避开的坑（一次读懂、不要再犯）

- **不要用 Streamlit / Dash / Plotly Dash**，除非用户明确要求。本 skill 的核心价值就是 Flask + ECharts 这套清晰分离的架构，部署到 nginx 后面更简单。
- **不要把所有数据硬编码到 HTML 里**。即使是静态数据也要走后端，这才是仪表盘可刷新的关键。
- **不要 `df.to_dict()` 直接当 JSON 返回**。pandas 的默认字典格式跟 ECharts 想要的格式不匹配，必须经过 `prepare_*_data()` 转换。
- **不要忘了 `host='0.0.0.0'`**。如果用户在容器或远程服务器跑，`127.0.0.1` 只能本机访问。
- **日期序列化坑**：`jsonify` 处理不了 `pd.Timestamp` 和 `datetime` 对象，必须先转字符串。
- **中文字体显示**：CSS 字体栈里加上 `"PingFang SC", "Microsoft YaHei"`，否则 macOS 和 Windows 的中文显示会不一致。模板里已经写好了。
