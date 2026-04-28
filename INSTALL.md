# 🎓 零基础安装指南

> 完全没装过 Python？没关系。本文档假设你**什么都没装过**，从头一步步教你跑起来。

---

## 第一部分：装 Python（如果你已经装过可以跳过）

### 怎么知道我装没装过？

打开终端，输入：

```bash
python --version
```

或者：

```bash
python3 --version
```

如果输出类似 `Python 3.11.5` 这样的版本号（**3.8 或更高版本都可以**），跳到第二部分。

如果提示 `command not found` 或者版本低于 3.8，按下面对应你的系统装一下。

> **怎么打开终端？**
> - **Mac**：按 `Cmd + 空格`，输入 "终端" 或 "Terminal"，回车
> - **Windows**：按 `Win + R`，输入 `powershell`，回车
> - **Linux**：你都用 Linux 了应该知道 😄

### 🍎 macOS 用户

**最简单的办法：用 Homebrew**

如果你没装过 Homebrew，先在终端运行（一行命令搞定）：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

按提示走完。然后装 Python：

```bash
brew install python
```

装完验证：

```bash
python3 --version
```

应该能看到版本号了。**注意 Mac 上要用 `python3` 而不是 `python`。**

### 🪟 Windows 用户

1. 浏览器打开 https://www.python.org/downloads/
2. 点击大大的黄色按钮 "Download Python 3.x.x"
3. 下载完双击安装包
4. **⚠️ 关键步骤**：在安装窗口最下方**勾选 "Add python.exe to PATH"**（这一步漏了后面所有命令都用不了）
5. 点 "Install Now"，等装完
6. 关掉所有终端窗口，**重新打开一个**（PATH 改了需要重启终端才生效）
7. 输入 `python --version` 验证

### 🐧 Linux 用户（Ubuntu/Debian）

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

---

## 第二部分：把仓库下载到本地

### 方式 A：用 Git（推荐，方便后续更新）

如果你装了 Git：

```bash
git clone https://github.com/YOUR_USERNAME/dashboard-builder.git
cd dashboard-builder
```

如果没装 Git，参考 https://git-scm.com/downloads 装一下。

### 方式 B：直接下载 ZIP（不用 Git 也行）

1. 浏览器打开仓库主页
2. 点绿色的 "Code" 按钮 → "Download ZIP"
3. 下载完解压到你想放的位置（比如桌面）
4. 终端 `cd` 到解压后的文件夹

---

## 第三部分：先跑 demo 验证环境

在跑 Skill 之前，先用 `demo/` 文件夹验证你的环境一切正常：

```bash
cd demo
pip install -r requirements.txt
python app.py
```

> Mac/Linux 上如果上面命令报错，把 `pip` 换成 `pip3`、`python` 换成 `python3` 试试。

终端会显示：

```
============================================================
仪表盘已启动！
浏览器打开：http://localhost:5000
按 Ctrl+C 停止
============================================================
```

浏览器打开 http://localhost:5000，应该能看到一个完整的气温仪表盘。

**看到了** → 环境 OK，继续第四部分装 Skill。
**没看到 / 报错** → 看 [skill/references/troubleshooting.md](skill/references/troubleshooting.md) 排查。

按 `Ctrl + C` 停止 demo。

---

## 第四部分：把 Skill 装进 Claude

不同的 Claude 客户端装法不一样，找到你用的那个：

### 选项 A：Claude.ai 网页版 / 移动 App

> 截至 2026 年 4 月，Claude.ai 的 Skills 功能在 Settings → Capabilities → Skills 里管理。具体 UI 可能随版本变化，以官方界面为准。

1. 把 `skill/` 文件夹整体打包成 zip：
   ```bash
   # 在仓库根目录运行
   cd skill && zip -r ../dashboard-builder-skill.zip . && cd ..
   ```
2. 打开 https://claude.ai
3. 右下角点你的头像 → Settings
4. 左边菜单找到 "Capabilities" 或 "Skills"
5. 点 "Upload skill" 或 "添加技能"，选刚才打包的 zip 文件
6. 等待几秒上传完成

> ⚠️ 如果你的 Claude.ai 账号没看到 Skills 入口，可能需要 Pro/Team 套餐。具体以 Anthropic 官方说明为准：https://docs.claude.com

### 选项 B：Claude Desktop 桌面端

1. 找到 Claude Desktop 的 Skills 目录：
   - **Mac**：`~/Library/Application Support/Claude/skills/`
   - **Windows**：`%APPDATA%\Claude\skills\`
   - **Linux**：`~/.config/Claude/skills/`
2. 如果目录不存在，自己创建一个
3. 把整个 `skill/` 文件夹复制进去，重命名为 `dashboard-builder`
4. 重启 Claude Desktop

### 选项 C：Claude Code 命令行

```bash
# 复制到全局 skills 目录
mkdir -p ~/.claude/skills
cp -r skill ~/.claude/skills/dashboard-builder
```

下次 `claude` 启动时会自动发现。

---

## 第五部分：第一次使用

打开 Claude，发以下消息测试：

> 我想做一个数据可视化仪表盘，演示一下你能怎么帮我？

如果 Skill 装对了，Claude 会回应你它准备按 dashboard-builder 工作流帮你设计仪表盘，会问你数据源、想看什么之类的问题。

或者直接让它做点真东西：

> 我有一份学生成绩 CSV，列是 学号、姓名、班级、科目、分数。帮我生成一个仪表盘项目，能看班级平均分对比、学科分布、成绩段分布。

Claude 会用 5-10 分钟生成完整项目放到输出目录，按它的指引下载就能跑。

---

## 🆘 卡住了？

按这个顺序排查：

1. 先看 [skill/references/troubleshooting.md](skill/references/troubleshooting.md)，里面整理了 12 个最常见报错
2. 在 GitHub 仓库提 Issue（用 Bug Report 模板，会引导你提供必需的信息）
3. 加入讨论区（如果仓库开了 Discussions）

绝大部分卡点都是「Python 没装好」「pip 装依赖失败」「端口被占」三类，troubleshooting 文档都覆盖了。

---

## 🎯 下一步

环境跑通后推荐顺序：

1. 详细读一遍 `demo/` 的代码（特别是 `app.py`），熟悉 Flask + Pandas 的基本套路
2. 改 `demo/app.py` 里的 `prepare_*_data()` 函数试试不同的数据处理（比如改成按"国家"分组而不是按"城市"）
3. 准备一份你自己的真实数据，让 Claude 帮你做仪表盘
4. 想部署到服务器？看 [skill/references/deployment.md](skill/references/deployment.md)
