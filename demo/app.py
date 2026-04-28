"""
全球城市气温仪表盘 — Demo 后端

这是一个完整可运行的示例，演示 dashboard-builder skill 生成的项目结构。
新手可以直接运行：
    pip install -r requirements.txt
    python app.py
然后浏览器打开 http://localhost:5000 查看效果。
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import os
from functools import lru_cache

app = Flask(__name__)


# ============================================================
# 数据加载（一次性读入内存，缓存复用）
# ============================================================
@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """加载 CSV 数据。lru_cache 让进程只读一次文件，加快后续请求响应。"""
    csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])  # 统一转成时间戳，方便后续按时间分组
    return df


# ============================================================
# 数据处理函数
# 每个函数对应一个 API，返回的字典会被 jsonify 序列化给前端
# ============================================================
def prepare_summary_data(df: pd.DataFrame) -> dict:
    """KPI 卡片数据：覆盖城市数、记录总数、最高温、最低温、十年升温幅度。"""
    # 计算每个城市每年的平均气温，用 2014 vs 2023 对比看十年升温
    yearly = df.groupby([df["date"].dt.year, "city"])["temp_c"].mean().reset_index()
    avg_2014 = yearly[yearly["date"] == 2014]["temp_c"].mean()
    avg_2023 = yearly[yearly["date"] == 2023]["temp_c"].mean()
    warming = round(float(avg_2023 - avg_2014), 2)

    return {
        "city_count": int(df["city"].nunique()),
        "record_count": int(len(df)),
        "max_temp": float(df["temp_c"].max()),
        "min_temp": float(df["temp_c"].min()),
        "warming_decade": warming,  # 十年升温℃
        "last_update": df["date"].max().strftime("%Y-%m-%d"),
    }


def prepare_timeline_data(df: pd.DataFrame) -> dict:
    """时间趋势：按月聚合的全球平均温度（10 年趋势线）。

    返回字段：
      dates       月份字符串列表
      values      每月全球平均温度
      moving_avg  12 个月移动平均（平滑趋势）
    """
    # 按月分组求平均
    monthly = df.set_index("date").resample("ME")["temp_c"].mean().round(2)
    # 12 个月移动平均，让长期趋势更直观
    moving = monthly.rolling(12, min_periods=1).mean().round(2)

    return {
        "dates": monthly.index.strftime("%Y-%m").tolist(),
        "values": monthly.tolist(),
        "moving_avg": moving.tolist(),
    }


def prepare_distribution_data(df: pd.DataFrame) -> dict:
    """分类分布：天气类型在所有记录中的占比。"""
    counts = df["weather"].value_counts()
    total = int(counts.sum())
    return {
        "categories": counts.index.tolist(),
        "values": counts.astype(int).tolist(),
        "percentages": (counts / total * 100).round(1).tolist(),
    }


def prepare_geo_data(df: pd.DataFrame) -> dict:
    """地理分布：每个城市的年均温 + 经纬度，前端用散点地图展示。"""
    # 取最近一年（2023）的城市平均温度
    latest_year = df[df["date"].dt.year == df["date"].dt.year.max()]
    by_city = latest_year.groupby(["city", "country", "latitude", "longitude"])["temp_c"].mean().round(1).reset_index()

    return {
        "cities": [
            {
                "name": row["city"],
                "country": row["country"],
                "lat": float(row["latitude"]),
                "lon": float(row["longitude"]),
                "temp": float(row["temp_c"]),
            }
            for _, row in by_city.iterrows()
        ]
    }


def prepare_city_ranking_data(df: pd.DataFrame) -> dict:
    """城市年均温排名：横向条形图用，按温度从高到低。"""
    latest_year = df[df["date"].dt.year == df["date"].dt.year.max()]
    ranking = latest_year.groupby("city")["temp_c"].mean().round(1).sort_values()
    return {
        "cities": ranking.index.tolist(),
        "temps": ranking.tolist(),
    }


# ============================================================
# 路由
# ============================================================
@app.route("/")
def index():
    """首页。把 summary 数据先渲染一份给模板，前端 JS 再异步刷新一次（兜底）。"""
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


@app.route("/api/ranking")
def api_ranking():
    return jsonify(prepare_city_ranking_data(load_data()))


@app.errorhandler(Exception)
def handle_error(e):
    """统一异常处理：日志记真错，返回前端的只是简短消息。"""
    app.logger.exception("API 出错")
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # host=0.0.0.0 允许同局域网其他设备访问；只想本机访问可改成 127.0.0.1
    print("=" * 60)
    print("仪表盘已启动！")
    print("浏览器打开：http://localhost:5000")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5004, debug=True)
