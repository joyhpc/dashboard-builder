# dashboard-builder Skill 结构解析

## 📁 完整目录结构

```
skill/
├── SKILL.md                          # 核心：Skill工作流定义（Claude读取）
│
├── assets/                           # 代码模板（生成项目时复制）
│   ├── backend/
│   │   ├── app_template.py          # Flask后端模板（142行）
│   │   └── requirements.txt         # Python依赖清单
│   └── frontend/
│       └── index_template.html      # 前端HTML模板（已修复路径）
│
└── references/                       # 参考文档（按需加载）
    ├── deployment.md                # 部署指南（nginx配置）
    ├── deployment-checklist.md      # 部署验证清单（新增）
    ├── troubleshooting.md           # 故障排查手册
    └── examples/                    # 场景案例库
        ├── README.md                # 案例索引
        ├── temperature.md           # 场景1：恶劣天气分布
        ├── lifespan.md              # 场景2：寿命分析
        ├── project.md               # 场景3：项目进度
        └── weather.md               # 场景4：疫情监控
```

**总计：** 12个文件，5个目录

---

## 🎯 核心文件：SKILL.md

### 作用
- **Claude读取的工作流定义**
- 定义Skill的执行步骤
- 包含提示词和决策逻辑

### 内容结构
```markdown
---
name: dashboard-builder
description: 5分钟搭出数据可视化仪表盘
---

# 工作流

## Step 1: 理解需求
- 询问用户数据源
- 确认关键指标

## Step 2: 选择图表
- 根据数据类型自动判断
- 时间序列 → 折线图
- 分类对比 → 柱状图
- 占比分布 → 饼图

## Step 3: 生成代码
- 复制 assets/ 模板
- 填充数据处理逻辑
- 生成完整项目

## Step 4: 部署指导
- 提供运行命令
- 引用 references/deployment.md
```

### 关键特性
- ✅ 定义Skill的"大脑"
- ✅ 控制执行流程
- ✅ 决定何时加载references

---

## 📦 assets/ - 代码模板库

### 作用
**生成项目时直接复制的模板文件**

### backend/app_template.py
```python
# 142行通用Flask框架
# 包含：
- load_data()           # 数据加载（支持多种数据源）
- prepare_*_data()      # 数据处理函数（TODO标记）
- API路由               # 标准化命名（/api/summary等）
```

**特点：**
- 填空式设计，用户只需实现TODO部分
- 支持Excel/CSV/API/数据库
- 已修复为相对路径 `fetch('api/')`

### backend/requirements.txt
```
flask
pandas
openpyxl
```

### frontend/index_template.html
```html
<!-- 完整的响应式前端 -->
- ECharts 5.4 CDN
- 深色主题样式
- KPI卡片布局
- 图表容器
- 数据加载逻辑（相对路径）
```

**特点：**
- 开箱即用的UI
- 移动端适配
- 已修复路径问题

---

## 📚 references/ - 参考文档库

### 作用
**按需加载的详细文档，不是每次都读取**

### deployment.md
```markdown
# 部署指南

## 本地开发
python app.py

## Nginx配置
location /dashboard/ {
    proxy_pass http://127.0.0.1:5000/;
}

## Gunicorn生产部署
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**何时加载：** 用户问"怎么部署"时

---

### deployment-checklist.md（新增）
```markdown
# 部署验证清单

## 本地测试
- [ ] python app.py 启动成功
- [ ] API返回JSON
- [ ] 浏览器控制台无错误

## Nginx部署
- [ ] nginx -t 通过
- [ ] 线上页面正常
- [ ] API路径正确
```

**何时加载：** 部署后验证时

---

### troubleshooting.md
```markdown
# 常见问题排查

## 502 Bad Gateway
原因：Flask未启动
解决：ps aux | grep python

## 数据加载失败
原因：API路径错误（绝对路径）
解决：改为相对路径
```

**何时加载：** 用户遇到错误时

---

### examples/ - 场景案例库

#### README.md
```markdown
# 4个典型场景

1. temperature.md - 恶劣天气分布
2. lifespan.md - 寿命分析
3. project.md - 项目进度
4. weather.md - 疫情监控
```

#### 每个案例包含
```markdown
## 数据结构
CSV格式，列名，数据类型

## 图表选择
- 时间趋势 → 折线图
- 地区对比 → 柱状图
- 占比分布 → 饼图

## 代码示例
完整的 prepare_*_data() 实现
```

**何时加载：** 用户数据类似某个场景时

---

## 🔄 文件间关系

```
用户请求
    ↓
SKILL.md（工作流）
    ↓
判断需求 → 选择场景
    ↓
加载 examples/xxx.md（可选）
    ↓
复制 assets/（必须）
    ├── app_template.py
    ├── requirements.txt
    └── index_template.html
    ↓
填充业务逻辑
    ↓
生成完整项目
    ↓
用户遇到问题？
    ↓
加载 references/troubleshooting.md
    ↓
用户要部署？
    ↓
加载 references/deployment.md
```

---

## 📊 加载策略

### 总是加载
- ✅ `SKILL.md` - 工作流定义
- ✅ `assets/*` - 代码模板

### 按需加载
- 🔄 `examples/*` - 数据类似时加载
- 🔄 `references/deployment.md` - 问部署时加载
- 🔄 `references/troubleshooting.md` - 遇到错误时加载
- 🔄 `references/deployment-checklist.md` - 验证时加载

---

## 🎯 设计原则

### 1. 分层设计
```
SKILL.md（核心逻辑）
    ↓
assets/（代码模板）
    ↓
references/（详细文档）
```

### 2. 按需加载
- 不是所有文档都每次读取
- 根据用户需求动态加载
- 减少token消耗

### 3. 模板化
- assets/ 是可复制的模板
- references/ 是可引用的文档
- examples/ 是可参考的案例

### 4. 可扩展
```
添加新场景：
└── references/examples/new-scenario.md

添加新文档：
└── references/new-guide.md

修改模板：
└── assets/backend/app_template.py
```

---

## 🔍 关键文件详解

### SKILL.md - 工作流引擎

**职责：**
1. 定义执行步骤
2. 决定何时加载references
3. 控制代码生成逻辑

**示例片段：**
```markdown
## Step 2: 分析数据类型

如果数据有时间列：
- 加载 examples/temperature.md 参考时间序列处理
- 生成折线图代码

如果数据有地理列：
- 加载 examples/weather.md 参考地图实现
- 生成地图代码
```

---

### app_template.py - 后端框架

**职责：**
1. 提供Flask基础结构
2. 定义标准API路由
3. 提供数据处理框架

**填空点：**
```python
def load_data():
    # TODO：改这里对接数据源
    pass

def prepare_summary_data(df):
    # TODO：计算KPI指标
    return {"total": 0}
```

---

### index_template.html - 前端框架

**职责：**
1. 提供响应式布局
2. 集成ECharts
3. 实现数据加载逻辑

**关键修复：**
```javascript
// ✅ 已修复为相对路径
fetch('api/summary')  // 支持子路径部署
```

---

## 💡 使用流程

### Claude执行Skill时

1. **读取 SKILL.md**
   - 理解工作流
   - 确定执行步骤

2. **分析用户需求**
   - 数据源类型
   - 关键指标
   - 图表需求

3. **选择性加载 examples/**
   - 数据有时间列 → 加载 temperature.md
   - 数据有地理列 → 加载 weather.md
   - 数据是项目管理 → 加载 project.md

4. **复制 assets/ 模板**
   - app_template.py → app.py
   - index_template.html → templates/index.html
   - requirements.txt → requirements.txt

5. **填充业务逻辑**
   - 实现 load_data()
   - 实现 prepare_*_data()
   - 删除不需要的API

6. **生成完整项目**
   - 输出到 outputs/ 目录
   - 提供运行命令

7. **按需提供文档**
   - 用户问部署 → 引用 deployment.md
   - 用户遇到错误 → 引用 troubleshooting.md
   - 用户要验证 → 引用 deployment-checklist.md

---

## 🎨 扩展示例

### 添加新场景案例

```bash
# 创建新案例
cat > skill/references/examples/sales.md << 'EOF'
# 销售数据仪表盘

## 数据结构
- 日期
- 销售员
- 产品类别
- 销售额
- 地区

## 图表选择
- 销售趋势：折线图
- 产品分布：饼图
- 地区对比：柱状图
- 销售员排名：条形图

## 代码示例
[完整实现...]
EOF
```

### 修改模板

```bash
# 修改后端模板
vim skill/assets/backend/app_template.py

# 修改前端模板
vim skill/assets/frontend/index_template.html
```

### 添加新文档

```bash
# 添加性能优化指南
cat > skill/references/performance.md << 'EOF'
# 性能优化指南

## 数据缓存
使用 @lru_cache

## 数据库索引
添加日期列索引

## 前端优化
ECharts按需加载
EOF
```

---

## 📈 文件大小统计

```bash
SKILL.md                    ~5KB   (工作流定义)
app_template.py            ~5KB   (142行代码)
index_template.html        ~8KB   (完整前端)
requirements.txt           ~50B   (3个依赖)
deployment.md              ~3KB   (部署指南)
deployment-checklist.md    ~4KB   (验证清单)
troubleshooting.md         ~3KB   (故障排查)
examples/*.md              ~2KB×4 (场景案例)

总计：~35KB
```

---

## 🎯 总结

### 核心三层

1. **SKILL.md** - 大脑（工作流）
2. **assets/** - 骨架（代码模板）
3. **references/** - 知识库（文档案例）

### 设计优势

✅ **模块化** - 每个文件职责清晰  
✅ **可扩展** - 易于添加新场景  
✅ **按需加载** - 减少token消耗  
✅ **填空式** - 用户只需实现业务逻辑  

### 当前状态

✅ 路径问题已修复  
✅ 部署验证清单已添加  
✅ 复盘报告已完成  
✅ 已同步到GitHub  

**Skill完全可用！** 🎉
