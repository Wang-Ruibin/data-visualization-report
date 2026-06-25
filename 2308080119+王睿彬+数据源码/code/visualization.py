import pandas as pd
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
OUT_DIR = BASE_DIR

df_users = pd.read_csv(os.path.join(DATA_DIR, "internet_users.csv"))
df_age = pd.read_csv(os.path.join(DATA_DIR, "age_structure.csv"))
df_edu = pd.read_csv(os.path.join(DATA_DIR, "education_structure.csv"))
df_app = pd.read_csv(os.path.join(DATA_DIR, "app_users.csv"))
df_ur = pd.read_csv(os.path.join(DATA_DIR, "urban_rural.csv"))
df_ip = pd.read_csv(os.path.join(DATA_DIR, "ip_addresses.csv"))

YEARS = df_users["年份"].tolist()
USERS = df_users["网民规模_亿"].tolist()
PENETRATION = df_users["互联网普及率_百分比"].tolist()
MOBILE_USERS = df_users["手机网民_亿"].tolist()
MOBILE_PCT = df_users["手机网民占比_百分比"].tolist()

ECHART_CDN = "https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/echarts.min.js"

options = []

def o(title_, opt):
    options.append({"title": title_, "option": json.dumps(opt, ensure_ascii=False)})


# Chart 1
o("中国网民规模与互联网普及率变化（2010-2025）", {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
    "legend": {"data": ["网民规模（亿）", "互联网普及率（%）"], "left": "center", "top": "bottom"},
    "xAxis": {"type": "category", "data": YEARS, "name": "年份"},
    "yAxis": [
        {"type": "value", "name": "网民规模（亿）", "min": 0, "axisLabel": {"formatter": "{value}亿"}},
        {"type": "value", "name": "互联网普及率（%）", "min": 0, "max": 100, "position": "right", "axisLabel": {"formatter": "{value}%"}},
    ],
    "series": [
        {"type": "bar", "name": "网民规模（亿）", "data": USERS, "itemStyle": {"color": "#5470C6"}, "label": {"show": True, "position": "top", "formatter": "{c}亿"}},
        {"type": "line", "name": "互联网普及率（%）", "data": PENETRATION, "yAxisIndex": 1, "lineStyle": {"width": 3, "color": "#91CC75"}, "itemStyle": {"color": "#91CC75"}, "label": {"show": True, "formatter": "{c}%"}, "areaStyle": {"opacity": 0.15, "color": "#91CC75"}},
    ],
})

# Chart 2
o("中国手机网民规模及占比变化（2010-2025）", {
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["手机网民规模（亿）", "手机网民占比（%）"], "left": "center", "top": "bottom"},
    "xAxis": {"type": "category", "data": YEARS, "name": "年份"},
    "yAxis": [
        {"type": "value", "name": "手机网民规模（亿）", "min": 0, "axisLabel": {"formatter": "{value}亿"}},
        {"type": "value", "name": "手机网民占比（%）", "min": 60, "max": 100, "position": "right", "axisLabel": {"formatter": "{value}%"}},
    ],
    "series": [
        {"type": "line", "name": "手机网民规模（亿）", "data": MOBILE_USERS, "lineStyle": {"width": 3, "color": "#5470C6"}, "itemStyle": {"color": "#5470C6"}, "label": {"show": True, "formatter": "{c}亿"}, "symbol": "circle", "symbolSize": 10, "areaStyle": {"opacity": 0.2, "color": "#5470C6"}},
        {"type": "line", "name": "手机网民占比（%）", "data": MOBILE_PCT, "yAxisIndex": 1, "lineStyle": {"width": 3, "type": "dashed", "color": "#EE6666"}, "itemStyle": {"color": "#EE6666"}, "label": {"show": True, "formatter": "{c}%"}, "symbol": "diamond", "symbolSize": 10},
    ],
})

# Chart 3
age_groups = list(df_age.columns[1:])
age_colors = ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE", "#3BA272", "#FC8452"]
age_series = []
for i, g in enumerate(age_groups):
    age_series.append({"type": "bar", "name": g, "data": df_age[g].tolist(), "stack": "age", "itemStyle": {"color": age_colors[i % len(age_colors)]}})
o("中国网民年龄结构演变（2013-2024）", {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {"data": age_groups, "left": "center", "top": "bottom"},
    "xAxis": {"type": "category", "data": df_age["年份"].astype(str).tolist(), "name": "年份"},
    "yAxis": {"type": "value", "name": "占比（%）", "axisLabel": {"formatter": "{value}%"}},
    "series": age_series,
})

# Chart 4
edu_groups = list(df_edu.columns[1:])
edu_colors = ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE"]
last_edu = df_edu.iloc[-1]
edu_pairs = [{"name": g, "value": last_edu[g]} for g in edu_groups]
o("2024年中国网民学历结构分布", {
    "tooltip": {"trigger": "item", "formatter": "{b}: {c}% ({d}%)"},
    "legend": {"data": edu_groups, "orient": "vertical", "left": "left", "top": "center"},
    "series": [{
        "type": "pie", "radius": ["35%", "60%"], "center": ["55%", "55%"],
        "data": edu_pairs, "label": {"formatter": "{b}: {d}%"},
        "itemStyle": {"borderColor": "#fff", "borderWidth": 2},
    }],
})

# Chart 5
df_app_sorted = df_app.sort_values("用户规模_亿")
apps = df_app_sorted["应用类别"].tolist()
app_vals = df_app_sorted["用户规模_亿"].tolist()
o("2024年中国主要互联网应用用户规模排名", {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "xAxis": {"type": "value", "name": "用户规模（亿）", "axisLabel": {"formatter": "{value}亿"}},
    "yAxis": {"type": "category", "data": apps, "name": "应用类别", "axisLabel": {}},
    "series": [{
        "type": "bar", "data": app_vals,
        "label": {"show": True, "position": "right", "formatter": "{c}亿"},
        "itemStyle": {"color": {"type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0, "colorStops": [{"offset": 0, "color": "#5470C6"}, {"offset": 1, "color": "#91CC75"}]}},
    }],
})

# Chart 6
ur_years = df_ur["年份"].astype(str).tolist()
urban = df_ur["城镇普及率_百分比"].tolist()
rural = df_ur["农村普及率_百分比"].tolist()
o("中国城乡互联网普及率对比（2013-2024）", {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {"data": ["城镇普及率（%）", "农村普及率（%）"], "left": "center", "top": "bottom"},
    "xAxis": {"type": "category", "data": ur_years, "name": "年份"},
    "yAxis": {"type": "value", "name": "普及率（%）", "axisLabel": {"formatter": "{value}%"}},
    "series": [
        {"type": "bar", "name": "城镇普及率（%）", "data": urban, "itemStyle": {"color": "#5470C6"}, "label": {"show": True, "position": "top", "formatter": "{c}%"}},
        {"type": "bar", "name": "农村普及率（%）", "data": rural, "itemStyle": {"color": "#91CC75"}, "label": {"show": True, "position": "top", "formatter": "{c}%"}},
    ],
})

# Chart 7
ip_years = df_ip["年份"].astype(str).tolist()
ip4 = df_ip["IPv4_亿"].tolist()
ip6 = df_ip["IPv6_亿"].tolist()
o("中国IPv4/IPv6地址资源变化（2017-2024）", {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {"data": ["IPv4地址（亿）", "IPv6地址（亿）"], "left": "center", "top": "bottom"},
    "xAxis": {"type": "category", "data": ip_years, "name": "年份"},
    "yAxis": {"type": "value", "name": "地址数量（亿）", "axisLabel": {"formatter": "{value}亿"}},
    "series": [
        {"type": "bar", "name": "IPv4地址（亿）", "data": ip4, "itemStyle": {"color": "#5470C6"}, "label": {"show": True, "position": "top"}},
        {"type": "bar", "name": "IPv6地址（亿）", "data": ip6, "itemStyle": {"color": "#91CC75"}, "label": {"show": True, "position": "top"}},
    ],
})

html_parts = []

HEADER_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>中国互联网发展态势可视化分析（2010-2025）</title>
<script src="CDN_PLACEHOLDER"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #f5f7fa; font-family: "Microsoft YaHei", "PingFang SC", sans-serif; }
.header { text-align: center; padding: 40px 20px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.header h1 { font-size: 28px; margin-bottom: 8px; }
.header p { font-size: 14px; opacity: 0.85; }
.chart-wrap { background: white; margin: 20px auto; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 20px; max-width: 1240px; }
.chart-wrap h2 { font-size: 16px; color: #333; margin-bottom: 12px; padding-left: 12px; border-left: 4px solid #5470C6; }
.chart-container { width: 100%; height: 520px; }
</style>
</head>
<body>
<div class="header">
<h1>中国互联网发展态势可视化分析</h1>
<p>基于 CNNIC 数据 · 2010–2025</p>
</div>
""".replace("CDN_PLACEHOLDER", ECHART_CDN)
html_parts.append(HEADER_HTML)

for i, item in enumerate(options):
    html_parts.append(f"""<div class="chart-wrap">
<h2>图{i+1} {item['title']}</h2>
<div id="chart{i+1}" class="chart-container"></div>
</div>""")

html_parts.append("""<script>
""")
for i, item in enumerate(options):
    html_parts.append(f"""var chart{i+1} = echarts.init(document.getElementById('chart{i+1}'));
var option{i+1} = {item['option']};
chart{i+1}.setOption(option{i+1});
""")

html_parts.append("""window.addEventListener('resize', function() {
""")
for i in range(len(options)):
    html_parts.append(f"  chart{i+1}.resize();\n")
html_parts.append("""});
</script>
</body>
</html>""")

with open(os.path.join(OUT_DIR, "visualization.html"), "w", encoding="utf-8") as f:
    f.writelines(html_parts)

print(f"All {len(options)} charts saved to visualization.html")
