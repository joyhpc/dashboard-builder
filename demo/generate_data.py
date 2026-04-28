"""
生成 demo 用的全球城市气温数据。

数据特征：
  - 12 个城市，覆盖 5 大洲 + 北/南半球
  - 时间范围 2014-01-01 到 2023-12-31（10 年日度数据）
  - 基于真实年均温做基线，叠加季节性正弦波动 + 长期升温趋势 + 随机噪声
  - 总记录数 ~43800 行，CSV 体积约 2 MB

字段：
  date         日期 (YYYY-MM-DD)
  city         城市中文名
  country      国家中文名
  continent    所属大洲
  latitude     纬度（地图用）
  longitude    经度（地图用）
  temp_c       当日平均气温 (摄氏度，保留 1 位小数)
  weather      天气类型（晴/多云/雨/雪/雾，按温度和随机性分配）
"""

import csv
import math
import random
from datetime import date, timedelta

random.seed(42)  # 固定随机种子，每次生成结果一致

# 12 个城市：(中文名, 国家, 大洲, 纬度, 经度, 年均温℃, 年温差幅度℃)
CITIES = [
    ("北京",     "中国",     "亚洲",   39.90, 116.40, 13.0, 16.0),
    ("上海",     "中国",     "亚洲",   31.23, 121.47, 17.0, 11.0),
    ("东京",     "日本",     "亚洲",   35.68, 139.69, 16.0, 11.0),
    ("新加坡",   "新加坡",   "亚洲",    1.35, 103.82, 27.5,  1.5),
    ("孟买",     "印度",     "亚洲",   19.08,  72.88, 27.0,  4.0),
    ("伦敦",     "英国",     "欧洲",   51.51,  -0.13, 11.0,  7.0),
    ("巴黎",     "法国",     "欧洲",   48.86,   2.35, 12.0,  9.0),
    ("纽约",     "美国",     "北美",   40.71, -74.01, 13.0, 13.0),
    ("洛杉矶",   "美国",     "北美",   34.05,-118.24, 18.0,  6.0),
    ("圣保罗",   "巴西",     "南美",  -23.55, -46.63, 19.0,  5.0),
    ("悉尼",     "澳大利亚", "大洋洲", -33.87, 151.21, 18.0,  7.0),
    ("开普敦",   "南非",     "非洲",   -33.92,  18.42, 17.0,  6.0),
]

START_DATE = date(2014, 1, 1)
END_DATE   = date(2023, 12, 31)
WARMING_PER_YEAR = 0.04   # 每年升温 0.04℃（接近真实全球平均）


def daily_temp(city_info, d: date) -> float:
    """基于年均温 + 季节性正弦波 + 升温趋势 + 噪声生成单日温度。"""
    _, _, _, lat, _, base_avg, swing = city_info

    # 一年中第几天 (1..366)
    day_of_year = d.timetuple().tm_yday
    # 季节性波动：北半球 7 月最热，南半球反相
    phase = -math.pi / 2 if lat >= 0 else math.pi / 2
    seasonal = (swing / 2) * math.sin(2 * math.pi * day_of_year / 365 + phase)
    # 长期升温趋势
    years_since_start = (d - START_DATE).days / 365.25
    warming = WARMING_PER_YEAR * years_since_start
    # 日间随机噪声 (±2℃)
    noise = random.gauss(0, 1.5)
    return round(base_avg + seasonal + warming + noise, 1)


def classify_weather(temp: float, lat: float, d: date) -> str:
    """根据温度 + 季节 + 随机性给一个天气分类。简化模型，足够 demo 用。"""
    r = random.random()
    if temp < 0:
        return "雪" if r < 0.4 else ("多云" if r < 0.7 else "晴")
    if temp < 10:
        return "雨" if r < 0.25 else ("雾" if r < 0.35 else ("多云" if r < 0.7 else "晴"))
    if temp < 25:
        return "雨" if r < 0.20 else ("多云" if r < 0.55 else "晴")
    # 高温
    return "雨" if r < 0.15 else ("多云" if r < 0.35 else "晴")


def generate():
    rows = []
    d = START_DATE
    while d <= END_DATE:
        for city_info in CITIES:
            name, country, continent, lat, lon, _, _ = city_info
            t = daily_temp(city_info, d)
            w = classify_weather(t, lat, d)
            rows.append([d.isoformat(), name, country, continent, lat, lon, t, w])
        d += timedelta(days=1)

    out_path = "/home/claude/dashboard-builder/demo/data.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "city", "country", "continent",
                         "latitude", "longitude", "temp_c", "weather"])
        writer.writerows(rows)
    print(f"已生成 {len(rows)} 行数据 -> {out_path}")


if __name__ == "__main__":
    generate()
