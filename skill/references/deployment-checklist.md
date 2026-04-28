# 部署验证清单

## ✅ 本地测试

### 1. 启动服务
```bash
cd your-dashboard
python app.py
```

**预期结果：**
```
* Running on http://127.0.0.1:5000
```

### 2. 测试页面加载
```bash
curl -I http://localhost:5000
```

**预期结果：** `HTTP/1.1 200 OK`

### 3. 测试API接口
```bash
curl http://localhost:5000/api/summary
```

**预期结果：** 返回JSON数据

### 4. 浏览器测试
- 打开 http://localhost:5000
- 按F12打开开发者工具
- 检查Console标签页，**不应有红色错误**
- 确认图表正常显示

---

## ✅ Nginx子路径部署

### 1. 配置Nginx
```nginx
location /dashboard/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

**注意：** `proxy_pass` 末尾的 `/` 不能省略

### 2. 测试配置
```bash
sudo nginx -t
```

**预期结果：** `syntax is ok` 和 `test is successful`

### 3. 重载Nginx
```bash
sudo systemctl reload nginx
```

### 4. 测试页面访问
```bash
curl -I https://yourdomain.com/dashboard/
```

**预期结果：** `HTTP/2 200`

### 5. 测试API访问
```bash
curl https://yourdomain.com/dashboard/api/summary
```

**预期结果：** 返回JSON数据

### 6. 检查前端路径
```bash
curl https://yourdomain.com/dashboard/ | grep "fetch("
```

**预期结果：** 应该看到 `fetch('api/` 而不是 `fetch('/api/`

### 7. 浏览器端到端测试
- 打开 https://yourdomain.com/dashboard/
- 按F12打开开发者工具
- 切换到Network标签页
- 刷新页面
- 检查所有API请求状态码是否为200
- 切换到Console标签页，**不应有404或500错误**
- 确认图表正常显示数据

---

## ❌ 常见问题排查

### 问题1：502 Bad Gateway

**原因：** Flask服务未启动

**排查：**
```bash
ps aux | grep "python.*app.py"
```

**解决：**
```bash
cd your-dashboard
python app.py &
```

---

### 问题2：页面显示"数据加载失败"

**原因：** API路径错误（使用了绝对路径）

**排查：**
```bash
# 检查浏览器控制台是否有404错误
# 检查HTML中的fetch路径
curl https://yourdomain.com/dashboard/ | grep "fetch("
```

**解决：**
如果看到 `fetch('/api/`，需要改为相对路径：
```bash
sed -i "s|fetch('/api/|fetch('api/|g" templates/index.html
```

然后重启Flask服务。

---

### 问题3：图表不显示

**可能原因：**
1. ECharts CDN加载失败
2. JavaScript语法错误
3. API返回数据格式不对

**排查：**
1. 打开浏览器控制台查看错误信息
2. 检查Network标签页，确认ECharts CDN加载成功
3. 检查API返回的数据结构是否符合预期

---

### 问题4：端口被占用

**错误信息：** `Address already in use`

**排查：**
```bash
lsof -i :5000
```

**解决：**
```bash
# 杀掉占用端口的进程
kill -9 <PID>

# 或者换个端口
python app.py  # 修改 app.py 中的端口号
```

---

## 📋 验证通过标准

- [x] 本地 http://localhost:5000 正常访问
- [x] 本地API http://localhost:5000/api/summary 返回JSON
- [x] Nginx配置测试通过
- [x] 线上页面 https://domain.com/subpath/ 正常访问
- [x] 线上API https://domain.com/subpath/api/summary 返回JSON
- [x] 浏览器控制台无404/500错误
- [x] 所有图表正常显示数据

**全部通过 = 部署成功！** ✅
