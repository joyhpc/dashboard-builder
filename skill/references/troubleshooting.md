# 常见问题排查（Troubleshooting）

按报错信息搜索本文。每个问题都给最短解决方案。

## 🔴 启动相关

### `ModuleNotFoundError: No module named 'flask'`

依赖没装。先装：

```bash
pip install -r requirements.txt
```

如果你有多个 Python 版本（macOS 上常见），用：

```bash
python3 -m pip install -r requirements.txt
```

然后启动也用 `python3 app.py`。

---

### `ModuleNotFoundError: No module named 'openpyxl'`

读 `.xlsx` 文件需要这个库。`requirements.txt` 里有，重新装一次：

```bash
pip install openpyxl
```

如果你的数据是 `.csv`，可以把 `app.py` 里的 `pd.read_excel` 改成 `pd.read_csv`，就不需要 openpyxl 了。

---

### `Address already in use` / `端口 5000 已被占用`

5000 端口被别的程序占了（macOS 上 AirPlay 默认占用 5000）。两种办法：

**办法 1：换端口** —— 把 `app.py` 最后一行改成 `app.run(host="0.0.0.0", port=5001)`，重新启动。

**办法 2：杀掉占用进程**
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9
# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

---

### `python: command not found`

Python 没装或没加进 PATH。

- **Mac**：装 [Homebrew](https://brew.sh) 后 `brew install python`
- **Windows**：去 [python.org](https://www.python.org/downloads/) 下载安装包，**勾上 "Add Python to PATH"**
- **Linux (Ubuntu/Debian)**：`sudo apt install python3 python3-pip`

装完重开终端，`python --version` 或 `python3 --version` 应该能输出版本号。

---

## 🟡 数据相关

### `KeyError: 'date'` 或类似

`prepare_*_data()` 函数里引用的列名跟实际 CSV/Excel 里的不一样。

排查方法：在 `load_data()` 后加一行 `print(df.columns.tolist())`，重启服务，看终端输出的真实列名，然后改函数里引用的列名。

---

### 页面打开了但图表是空的

打开浏览器开发者工具（F12）→ Console 标签页，看红色报错。常见两种：

**`Failed to fetch /api/xxx`**：后端报错了。看你启动 Flask 的那个终端窗口，找最近的红色 traceback。八成是 `prepare_*_data()` 里某行报错。

**`TypeError: Cannot read properties of undefined`**：后端返回的字段名跟前端预期的不一致。比如后端返回 `{"data": [...]}` 但前端读的是 `data.values`。对照接口返回的实际 JSON 修改前端 `init*Chart()` 里的字段引用。

直接看接口长啥样：浏览器访问 `http://localhost:5000/api/summary`，能看到 JSON。

---

### `TypeError: Object of type Timestamp is not JSON serializable`

经典 pandas 坑。`jsonify` 处理不了 pandas 的 Timestamp 对象。

在返回前先把日期转字符串：

```python
# 错的
return {"dates": df["date"].tolist()}
# 对的
return {"dates": df["date"].dt.strftime("%Y-%m-%d").tolist()}
```

如果是单个 Timestamp 字段，用：

```python
return {"last_update": df["date"].max().strftime("%Y-%m-%d")}
```

---

### `TypeError: Object of type int64 is not JSON serializable`

pandas / numpy 的数值类型也会触发。包一层 `int()` 或 `float()`：

```python
# 错的
return {"total": df["amount"].sum()}
# 对的
return {"total": int(df["amount"].sum())}
```

---

### CSV 读出来中文乱码

```python
# 试试不同编码
df = pd.read_csv("data.csv", encoding="utf-8")
# 还乱码就改成
df = pd.read_csv("data.csv", encoding="gbk")
```

GBK 主要在 Windows 导出的 CSV 里出现。

---

## 🟢 显示相关

### 图表标签显示成方框

中文字体没加载到。HTML 模板的 `<style>` 里 `font-family` 加上：

```css
font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
```

---

### 图表大小不对 / 图表挤在一起

ECharts 需要在 div 渲染完成后才能正确测量尺寸。两种办法：

1. 确认 `<div class="chart">` 有明确的 `height`（CSS 里设了 `height: 360px;`）
2. 浏览器窗口缩放后图变形 → 模板已经处理了 `window.addEventListener('resize', () => chart.resize())`，没复制全的话补上

---

### CDN 加载慢，echarts 长时间不出来

国内访问 jsdelivr 偶尔慢。换成国内镜像：

```html
<!-- 把 -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<!-- 改成 -->
<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
```

---

## ⚪ 还是搞不定？

带上以下三样东西到仓库提 issue：

1. **完整报错信息**（终端输出的 traceback 或浏览器 console 截图）
2. **数据文件的前 5 行**（用 `df.head().to_dict()` 输出，注意脱敏）
3. **你做了什么**（一句话说清复现步骤）
