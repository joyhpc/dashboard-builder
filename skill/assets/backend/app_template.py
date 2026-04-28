"""
Dashboard Builder skill 的 Flask 后端模板。

复制此文件到输出目录命名为 app.py，然后：
  1. 改 load_data() 函数体，对接你的实际数据源
  2. 实现你需要的几个 prepare_*_data() 函数（不需要的删掉）
  3. 删掉对应的 /api/* 路由（如果你不用某个接口）

完整跑通的示例见 demo/ 目录。
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import glob
import os
from functools import lru_cache

app = Flask(__name__)


# ============================================================
# 数据加载 —— 改这里对接你的数据源
# ============================================================
@lru_cache(maxsize=1)
def load_data():
    """缓存式加载。lru_cache 让进程只读一次文件。
    如果是实时数据源（比如每次都要查 API），把装饰器删掉。"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # --- 方式 1：Excel ---
    xlsx_files = glob.glob(os.path.join(base_dir, "*.xlsx"))
    if xlsx_files:
        return pd.read_excel(xlsx_files[0])

    # --- 方式 2：CSV ---
    # csv_files = glob.glob(os.path.join(base_dir, "*.csv"))
    # if csv_files:
    #     return pd.read_csv(csv_files[0])

    # --- 方式 3：SQLite 数据库 ---
    # import sqlite3
    # conn = sqlite3.connect(os.path.join(base_dir, "data.db"))
    # return pd.read_sql("SELECT * FROM your_table", conn)

    # --- 方式 4：HTTP API ---
    # import requests
    # r = requests.get("https://api.example.com/data", timeout=10)
    # return pd.DataFrame(r.json())

    raise FileNotFoundError("没找到数据源。请修改 load_data() 函数。")


# ============================================================
# 数据处理函数 —— 用到哪个写哪个
# 每个返回的字典会被 jsonify 序列化给前端
# ============================================================
def prepare_summary_data(df: pd.DataFrame) -> dict:
    """KPI 卡片数据。永远要实现这个。
    返回的字段名必须跟 HTML 模板里 KPI 卡片的 id 对应。"""
    # TODO：根据实际数据替换
    return {
        "total": int(len(df)),
        "max": None,
        "min": None,
        "avg": None,
        "last_update": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
    }


def prepare_timeline_data(df: pd.DataFrame) -> dict:
    """时间序列。如果数据有日期列就实现。
    重要：必须把 Timestamp 转成字符串，jsonify 处理不了原生时间戳。"""
    # TODO：把下面的注释取消并改成实际列名
    # df['date'] = pd.to_datetime(df['date'])
    # grouped = df.groupby(df['date'].dt.date)['value'].sum().reset_index()
    # return {
    #     "dates": grouped['date'].astype(str).tolist(),
    #     "values": grouped['value'].tolist(),
    #     "moving_avg": grouped['value'].rolling(7, min_periods=1).mean().round(2).tolist(),
    # }
    return {"dates": [], "values": [], "moving_avg": []}


def prepare_distribution_data(df: pd.DataFrame) -> dict:
    """分类分布。如果数据有分类列就实现。"""
    # TODO：改成实际的分类列名
    # counts = df['category'].value_counts()
    # total = counts.sum()
    # return {
    #     "categories": counts.index.tolist(),
    #     "values": counts.tolist(),
    #     "percentages": (counts / total * 100).round(1).tolist(),
    # }
    return {"categories": [], "values": [], "percentages": []}


def prepare_geo_data(df: pd.DataFrame) -> dict:
    """地理数据。如果数据有地点列就实现。"""
    # TODO
    return {"regions": [], "values": []}


# ============================================================
# 路由 —— 不用的接口直接删
# ============================================================
@app.route("/")
def index():
    df = load_data()
    summary = prepare_summary_data(df)
    return render_template("index.html", summary=summary)


@app.route("/api/summary")
def api_summary():
    return jsonify(prepare_summary_data(load_data()))


@app.route("/api/timeline")
def api_timeline():
    return jsonify(prepare_timeline_data(load_data()))


@app.route("/api/distribution")
def api_distribution():
    return jsonify(prepare_distribution_data(load_data()))


@app.route("/api/geo")
def api_geo():
    return jsonify(prepare_geo_data(load_data()))


@app.errorhandler(Exception)
def handle_error(e):
    """统一异常处理：服务端记真错，给前端只返回简单消息。"""
    app.logger.exception("API 出错")
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # host=0.0.0.0 让局域网其他设备也能访问；只想本机访问改成 127.0.0.1
    app.run(host="0.0.0.0", port=5000, debug=True)
