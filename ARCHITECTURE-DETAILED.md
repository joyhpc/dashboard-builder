# dashboard-builder 详细架构与流程

## 📐 整体架构

### 系统分层

```
┌─────────────────────────────────────────────────────────┐
│                    浏览器层                              │
│  - 用户交互界面                                          │
│  - 图表渲染引擎                                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────────┐
│                  Nginx反向代理                           │
│  - SSL终止                                               │
│  - 负载均衡                                              │
│  - 静态资源缓存                                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────────┐
│                  Flask应用层                             │
│  - 路由控制                                              │
│  - 业务逻辑                                              │
│  - 数据处理                                              │
└────────────────────┬────────────────────────────────────┘
                     │ Pandas DataFrame
┌────────────────────▼────────────────────────────────────┐
│                   数据源层                               │
│  - Excel/CSV文件                                         │
│  - 关系型数据库                                          │
│  - HTTP API                                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 前端架构

### 技术栈

**核心库：**
- ECharts 5.4.3 - 图表渲染引擎
- 原生JavaScript - 无框架依赖
- CSS3 - 响应式布局

**为什么不用React/Vue？**
- 减少打包体积（0KB vs 100KB+）
- 降低学习成本（原生JS人人会）
- 加快首屏加载（无需解析框架）

### 页面结构

```html
<!DOCTYPE html>
<html>
<head>
    <script src="echarts.min.js"></script>  <!-- CDN加载 -->
    <style>/* 响应式样式 */</style>
</head>
<body>
    <!-- 1. KPI指标卡片区 -->
    <div class="metrics-row">
        <div class="metric-card">
            <div class="label">总销售额</div>
            <div class="value" id="total">-</div>
        </div>
    </div>
    
    <!-- 2. 图表容器区 -->
    <div class="charts-grid">
        <div class="chart-wrapper">
            <h3>销售趋势</h3>
            <div class="chart" id="timeline-chart"></div>
        </div>
    </div>
    
    <script>/* 数据加载与渲染 */</script>
</body>
</html>
```

### 数据流

```javascript
// 1. 页面加载完成
window.addEventListener('DOMContentLoaded', () => {
    
    // 2. 并行请求所有API
    Promise.all([
        fetch('api/summary').then(r => r.json()),
        fetch('api/timeline').then(r => r.json()),
        fetch('api/distribution').then(r => r.json())
    ])
    
    // 3. 数据到达后渲染
    .then(([summary, timeline, distribution]) => {
        // 3.1 更新KPI卡片
        document.getElementById('total').textContent = summary.total;
        
        // 3.2 初始化图表
        initTimelineChart(timeline);
        initDistributionChart(distribution);
    })
    
    // 4. 错误处理
    .catch(err => {
        console.error('数据加载失败:', err);
        showErrorMessage('请检查后端是否启动');
    });
});
```

### 图表初始化

```javascript
function initTimelineChart(data) {
    const chart = echarts.init(document.getElementById('timeline-chart'));
    
    chart.setOption({
        // 提示框配置
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(0,0,0,0.8)',
            textStyle: { color: '#fff' }
        },
        
        // 图例配置
        legend: {
            data: ['销售额', '7日均线'],
            textStyle: { color: '#fff' }
        },
        
        // X轴配置
        xAxis: {
            type: 'category',
            data: data.dates,  // ['2024-01-01', '2024-01-02', ...]
            axisLabel: { 
                color: '#fff',
                rotate: 45  // 日期倾斜显示
            }
        },
        
        // Y轴配置
        yAxis: {
            type: 'value',
            axisLabel: { color: '#fff' }
        },
        
        // 数据系列
        series: [
            {
                name: '销售额',
                type: 'bar',
                data: data.values,  // [1200, 1500, 1800, ...]
                itemStyle: { color: '#5470c6' }
            },
            {
                name: '7日均线',
                type: 'line',
                data: data.moving_avg,
                smooth: true,
                itemStyle: { color: '#fac858' }
            }
        ]
    });
}
```

### 响应式设计

```css
/* 移动端适配 */
@media (max-width: 768px) {
    .metrics-row {
        grid-template-columns: repeat(2, 1fr);  /* 2列布局 */
    }
    
    .charts-grid {
        grid-template-columns: 1fr;  /* 单列布局 */
    }
    
    .chart {
        height: 250px;  /* 降低图表高度 */
    }
}

/* 桌面端 */
@media (min-width: 769px) {
    .metrics-row {
        grid-template-columns: repeat(4, 1fr);  /* 4列布局 */
    }
    
    .charts-grid {
        grid-template-columns: repeat(2, 1fr);  /* 2列布局 */
    }
    
    .chart {
        height: 350px;
    }
}
```

---

## 🔧 后端架构

### Flask应用结构

```python
from flask import Flask, render_template, jsonify
import pandas as pd
from functools import lru_cache

app = Flask(__name__)

# ============================================================
# 1. 数据加载层
# ============================================================
@lru_cache(maxsize=1)  # 缓存：只读一次文件
def load_data():
    """数据加载入口，支持多种数据源"""
    df = pd.read_csv('data.csv', parse_dates=['日期'])
    return df

# ============================================================
# 2. 数据处理层
# ============================================================
def prepare_summary_data(df):
    """计算KPI指标"""
    return {
        "total": int(df['销售额'].sum()),
        "avg": int(df['销售额'].mean()),
        "max": int(df['销售额'].max()),
        "count": len(df)
    }

def prepare_timeline_data(df):
    """时间序列数据处理"""
    # 按日期分组聚合
    daily = df.groupby('日期')['销售额'].sum().reset_index()
    
    # 计算移动平均
    daily['移动平均'] = daily['销售额'].rolling(7, min_periods=1).mean()
    
    return {
        "dates": daily['日期'].dt.strftime('%Y-%m-%d').tolist(),
        "values": daily['销售额'].tolist(),
        "moving_avg": daily['移动平均'].round(0).tolist()
    }

# ============================================================
# 3. 路由控制层
# ============================================================
@app.route('/')
def index():
    """首页路由"""
    return render_template('index.html')

@app.route('/api/summary')
def api_summary():
    """KPI指标API"""
    df = load_data()
    return jsonify(prepare_summary_data(df))

@app.route('/api/timeline')
def api_timeline():
    """时间序列API"""
    df = load_data()
    return jsonify(prepare_timeline_data(df))

# ============================================================
# 4. 应用启动
# ============================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 数据处理流程

```
原始数据 (CSV/Excel)
    ↓
Pandas读取
    ↓
DataFrame对象
    ↓
数据清洗
├─ 日期解析: pd.to_datetime()
├─ 缺失值处理: fillna()
└─ 类型转换: astype()
    ↓
数据聚合
├─ 分组: groupby()
├─ 统计: sum()/mean()/count()
└─ 透视: pivot_table()
    ↓
结果转换
├─ 转列表: .tolist()
├─ 转字典: .to_dict()
└─ 日期格式化: strftime()
    ↓
JSON序列化
    ↓
HTTP响应
```

### 缓存机制

```python
from functools import lru_cache

# 方案1：函数级缓存（适合静态数据）
@lru_cache(maxsize=1)
def load_data():
    return pd.read_csv('data.csv')  # 只执行一次

# 方案2：时间过期缓存（适合定期更新）
import time

cache = {"data": None, "timestamp": 0}

def load_data_with_ttl(ttl=300):  # 5分钟过期
    now = time.time()
    if cache["data"] is None or now - cache["timestamp"] > ttl:
        cache["data"] = pd.read_csv('data.csv')
        cache["timestamp"] = now
    return cache["data"]

# 方案3：Redis缓存（适合分布式）
import redis
import pickle

r = redis.Redis()

def load_data_from_redis():
    cached = r.get('dashboard_data')
    if cached:
        return pickle.loads(cached)
    
    df = pd.read_csv('data.csv')
    r.setex('dashboard_data', 300, pickle.dumps(df))
    return df
```

---

## 🗄️ 数据源层

### 支持的数据源

#### 1. CSV文件
```python
def load_data():
    return pd.read_csv('data.csv', 
                       encoding='utf-8-sig',  # 处理中文BOM
                       parse_dates=['日期'])   # 自动解析日期
```

#### 2. Excel文件
```python
def load_data():
    return pd.read_excel('data.xlsx',
                         sheet_name='Sheet1',
                         engine='openpyxl')
```

#### 3. SQLite数据库
```python
import sqlite3

def load_data():
    conn = sqlite3.connect('data.db')
    df = pd.read_sql("""
        SELECT 日期, 销售额, 产品类别
        FROM sales
        WHERE 日期 >= '2024-01-01'
    """, conn)
    conn.close()
    return df
```

#### 4. MySQL数据库
```python
from sqlalchemy import create_engine

def load_data():
    engine = create_engine('mysql://user:pass@localhost/db')
    return pd.read_sql('SELECT * FROM sales', engine)
```

#### 5. HTTP API
```python
import requests

def load_data():
    r = requests.get('https://api.example.com/sales', timeout=10)
    return pd.DataFrame(r.json())
```

### 数据格式要求

**标准格式：**
```csv
日期,销售额,产品类别,地区
2024-01-01,1200,电子产品,华东
2024-01-02,1500,服装,华南
```

**必须包含：**
- 至少1个数值列（用于计算KPI）
- 可选：日期列（用于时间序列）
- 可选：分类列（用于分布图）
- 可选：地理列（用于地图）

---

## 🔄 完整数据流

### 用户请求流程

```
1. 用户打开浏览器
   └─ https://domain.com/dashboard/

2. Nginx接收请求
   ├─ SSL解密
   ├─ 路径重写: /dashboard/ → /
   └─ 转发到Flask: http://127.0.0.1:5000/

3. Flask处理请求
   ├─ 路由匹配: @app.route('/')
   ├─ 渲染模板: render_template('index.html')
   └─ 返回HTML

4. 浏览器接收HTML
   ├─ 解析DOM
   ├─ 加载ECharts CDN
   └─ 执行JavaScript

5. JavaScript发起API请求
   ├─ fetch('api/summary')
   ├─ fetch('api/timeline')
   └─ fetch('api/distribution')

6. Flask处理API请求
   ├─ 加载数据: load_data()
   ├─ 处理数据: prepare_*_data()
   └─ 返回JSON

7. JavaScript接收数据
   ├─ 更新KPI卡片
   └─ 初始化ECharts图表

8. 用户看到完整仪表盘
```

### 性能优化点

```
1. 数据加载层
   ├─ @lru_cache: 缓存DataFrame
   └─ 只读必要列: usecols=['日期', '销售额']

2. 数据处理层
   ├─ 向量化操作: df['销售额'].sum()
   └─ 避免循环: 用groupby代替for

3. 网络传输层
   ├─ GZIP压缩: Flask自动启用
   └─ 减少数据量: 只返回必要字段

4. 前端渲染层
   ├─ 并行请求: Promise.all()
   └─ 按需渲染: 只初始化可见图表
```

---

## 🚀 部署架构

### 开发环境

```bash
# 单进程Flask
python app.py

# 特点：
- 自动重载代码
- 详细错误信息
- 单线程处理请求
- 不适合生产
```

### 生产环境

```bash
# Gunicorn多进程
gunicorn -w 4 -b 127.0.0.1:5000 app:app

# 参数说明：
-w 4          # 4个worker进程
-b 127.0.0.1  # 绑定本地地址
--timeout 30  # 请求超时30秒
--access-logfile logs/access.log  # 访问日志
```

### Nginx配置

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL证书
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # 仪表盘路由
    location /dashboard/ {
        # 反向代理到Flask
        proxy_pass http://127.0.0.1:5000/;
        
        # 请求头转发
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 进程管理

```bash
# Systemd服务配置
cat > /etc/systemd/system/dashboard.service << 'EOF'
[Unit]
Description=Dashboard Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/dashboard
ExecStart=/var/www/dashboard/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
