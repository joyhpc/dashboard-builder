# 部署指南

只在用户问起部署、上线、nginx、gunicorn 时读这个文档。

## 生产服务器：用 gunicorn，不要用 `python app.py`

Flask 自带的开发服务器是单线程、不安全的，生产环境必须换成 gunicorn：

```bash
# 安装
pip install gunicorn

# 启动（2 个 worker，绑定 localhost 让 nginx 转发）
gunicorn -w 2 -b 127.0.0.1:5001 app:app --daemon

# 带日志
gunicorn -w 2 -b 127.0.0.1:5001 app:app \
    --access-logfile access.log \
    --error-logfile error.log \
    --daemon
```

worker 数经验值：`(2 × CPU 核心数) + 1`。小型仪表盘 2 个就够。

## nginx 反向代理

加到 nginx 配置（通常在某个 `server { ... }` 块里）：

```nginx
location /your-dashboard/ {
    proxy_pass http://127.0.0.1:5001/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

`location` 和 `proxy_pass` 后面的斜杠都很重要——会在转发前剥掉 `/your-dashboard/` 前缀。

如果用子路径而不是子域名，前端的 `fetch()` 调用要带前缀，或者用 Flask 的 `APPLICATION_ROOT` 配合 `url_for()` 而不是硬编码 `/api/...`。

## systemd 自启动（重启后服务自动起来）

`/etc/systemd/system/dashboard.service`：

```ini
[Unit]
Description=Dashboard
After=network.target

[Service]
User=www-data
WorkingDirectory=/srv/dashboard
ExecStart=/srv/dashboard/venv/bin/gunicorn -w 2 -b 127.0.0.1:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启用：`systemctl enable dashboard && systemctl start dashboard`

## HTTPS

用 Let's Encrypt + certbot，免费自动续期。**TLS 在 nginx 层处理，不要在 Flask 里搞**。

## 常见部署坑

- **静态文件**：如果加了 `/static/` 下的 CSS/JS，让 nginx 直接服务（更快），别让 Flask 处理
- **数据文件路径**：gunicorn 的工作目录可能跟 dev 时不同。用 `os.path.dirname(__file__)` 做绝对路径
- **CORS**：只有前端和 API 不在同一个域名时才需要配 CORS。同一个 nginx 下不需要管这个
