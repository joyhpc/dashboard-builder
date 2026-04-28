# 📊 dashboard-builder

> 一个让 Claude 帮你**5 分钟搭出数据可视化仪表盘**的 Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange.svg)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)

把这个 Skill 装进 Claude 后，你只需要扔给 Claude 一份数据（Excel / CSV / API）说"帮我做个仪表盘"，它会自动按统一的最佳实践生成完整可部署的 Flask + ECharts 项目——后端、前端、依赖文件、README 一应俱全。

## 这是什么

**一句话版本**：把"我有一份数据，能不能做个图表网页给我看？"这种需求，从需要看半天教程的工程任务，变成跟 Claude 说一句话的事情。

**它做什么**：
- 自动判断你的数据该用什么图表（折线 / 柱状 / 饼图 / 散点 / 地理…）
- 生成完整的 Flask 后端（不是简单脚本，是有清晰 API 设计的项目）
- 生成响应式深色主题前端（手机也能看）
- 给你部署到 nginx 后面的现成配置
- 处理好新手最容易踩的坑（中文乱码、日期序列化、CDN 选择等）

**它不做什么**：
- 不取代 Tableau / PowerBI（人家是 SaaS，这是自己跑的代码）
- 不画一次性的静态图（那个用 matplotlib 一行就够）
- 不做花哨的 3D 数据艺术（这是给业务看的看板，不是 demo reel）

---

## ⚡ 30 秒看效果

仓库里 `demo/` 是一个完整可跑的示例（全球城市气温分析），不需要装 Skill 就能跑：

```bash
git clone https://github.com/YOUR_USERNAME/dashboard-builder.git
cd dashboard-builder/demo
pip install -r requirements.txt
python app.py
```

浏览器打开 http://localhost:5000，你会看到：

> _截图位置：`demo/screenshots/dashboard.png`_

包含 5 个 KPI 卡片、月平均气温趋势图、城市排名、天气分布、地理散点图。完整文件结构和代码可以直接对照学。

---

## 📐 系统架构

### 整体框架

![Dashboard Builder系统框架图](Dashboard%20Builder系统框架图.png)

**三层架构：**
- **前端层** - ECharts图表渲染 + 响应式布局
- **应用层** - Flask路由控制 + Pandas数据处理
- **数据层** - 多源支持（Excel/CSV/API/数据库）

### 业务数据流

![Dashboard Builder业务数据流图](Dashboard%20Builder业务数据流图.png)

**完整链路：**
1. 用户提供数据源
2. Claude分析数据结构
3. 生成Flask后端 + ECharts前端
4. 部署到nginx
5. 用户访问仪表盘

详细架构说明见 [ARCHITECTURE-DETAILED.md](ARCHITECTURE-DETAILED.md)

## 🚀 用起来 —— 三步

### 1. 把 Skill 装进 Claude

详细教程见 **[INSTALL.md](INSTALL.md)**（含 Claude Desktop / Claude.ai / Claude Code 三个环境的图文步骤）。

最简版本：把 `skill/` 目录作为一个 Skill 加到你的 Claude 客户端。

### 2. 跟 Claude 说话

打开任意 Claude 对话窗口，发：

> 我有一份销售数据 sales.xlsx，列是日期、销售员、产品类别、金额、地区。帮我做一个仪表盘。

或者更简单：

> [拖一个 CSV 进来] 帮我把这份数据可视化。

Claude 会读取 Skill 自动按 5 步流程生成项目，过程中可能会问你 1-2 个关键问题（比如「你最关心哪几个指标」）。

### 3. 跑生成的项目

Claude 会把项目放到 `outputs/<项目名>/`。

```bash
cd outputs/your-dashboard
pip install -r requirements.txt
python app.py
```

打开 http://localhost:5000 完事。

---

## 🧩 为什么是 Flask + ECharts

短答：**部署最简单、定制最自由、新手最不容易卡住**。

| 方案 | 上手难度 | 部署难度 | 定制自由度 |
|---|---|---|---|
| **Flask + ECharts**（本项目）| 低 | 低（一个 Python 脚本 + nginx 转发）| 高 |
| Streamlit | 极低 | 中（专用部署模式）| 低（被框架限制）|
| Dash | 中 | 中 | 中 |
| Tableau / PowerBI | 中 | 不需要 | 中（受限于平台）|
| 纯 React + D3 | 高 | 高 | 极高 |

我们选这套是因为：**新手能看懂每一行代码**（不像 Streamlit 把所有逻辑藏在框架里），**部署一条 nginx 配就够**（不像 React 要打包构建链），**ECharts 中文文档完整**（不像 D3 学习曲线陡）。

---

## 📚 文档

- **[INSTALL.md](INSTALL.md)** —— 把 Skill 装进 Claude 的保姆级教程
- **[demo/README.md](demo/README.md)** —— 完整示例项目说明
- **[skill/SKILL.md](skill/SKILL.md)** —— Skill 主文件（给 Claude 看的工作流）
- **[skill/references/troubleshooting.md](skill/references/troubleshooting.md)** —— 新手常见报错排查
- **[skill/references/deployment.md](skill/references/deployment.md)** —— 生产部署（gunicorn + nginx）
- **[CONTRIBUTING.md](CONTRIBUTING.md)** —— 想贡献代码看这里

---

## 📁 仓库结构

```
dashboard-builder/
├── README.md             ← 你正在看这个
├── INSTALL.md            ← 怎么装 Skill 到 Claude（零基础友好）
├── LICENSE               ← MIT
├── CONTRIBUTING.md       ← 贡献指南
│
├── skill/                ← Skill 本体（要装到 Claude 的就是这部分）
│   ├── SKILL.md          ← 给 Claude 看的工作流
│   ├── assets/           ← 代码模板（后端 + 前端）
│   └── references/       ← 详细参考文档（按需加载）
│       ├── examples/     ← 4 个典型场景案例
│       ├── deployment.md
│       └── troubleshooting.md
│
├── demo/                 ← 完整可跑的示例项目（全球气温仪表盘）
│   ├── app.py
│   ├── data.csv          ← 4.4 万条合成数据
│   ├── templates/index.html
│   ├── requirements.txt
│   └── README.md
│
└── .github/              ← Issue 模板、PR 模板
```

---

## 🤝 贡献

欢迎 PR 和 issue。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

特别欢迎的贡献：
- 新的参考案例（比如电商销售、金融交易、运动数据等不同形态）
- troubleshooting 文档补充新的报错场景
- 翻译（目前是中文为主，欢迎英文版 README）
- demo 截图（仓库里目前是占位符）

## 📜 License

MIT —— 商用、修改、二次发布都可以，标注一下出处即可。详见 [LICENSE](LICENSE)。

## 🙏 致谢

- 灵感来源：作者的疫情数据可视化项目实战经验
- 技术栈：[Flask](https://flask.palletsprojects.com/) + [Apache ECharts](https://echarts.apache.org/) + [Pandas](https://pandas.pydata.org/)
- 由 [Claude](https://claude.ai) 协助构建
