import pandas as pd
from pyecharts.charts import Bar, Line, Pie, Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType, CurrentConfig
from pyecharts.commons.utils import JsCode
import os

CurrentConfig.ONLINE_HOST = "https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
OUT_DIR = BASE_DIR

df_users = pd.read_csv(os.path.join(DATA_DIR, "internet_users.csv"))
df_age = pd.read_csv(os.path.join(DATA_DIR, "age_structure.csv"))
df_edu = pd.read_csv(os.path.join(DATA_DIR, "education_structure.csv"))
df_app = pd.read_csv(os.path.join(DATA_DIR, "app_users.csv"))
df_ur = pd.read_csv(os.path.join(DATA_DIR, "urban_rural.csv"))
df_ip = pd.read_csv(os.path.join(DATA_DIR, "ip_addresses.csv"))

years = df_users["年份"].tolist()
users = df_users["网民规模_亿"].tolist()
penetration = df_users["互联网普及率_百分比"].tolist()
mobile_users = df_users["手机网民_亿"].tolist()
mobile_pct = df_users["手机网民占比_百分比"].tolist()


def make_chart1():
    bar = Bar(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart1"
    ))
    bar.add_xaxis(years)
    bar.add_yaxis(
        "网民规模（亿）", users,
        yaxis_index=0,
        itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),
        label_opts=opts.LabelOpts(is_show=True, position="top",
                                   formatter=JsCode("function(p){return p.data + '亿';}"))
    )
    bar.extend_axis(
        yaxis=opts.AxisOpts(
            name="互联网普及率（%）",
            type_="value",
            min_=0,
            max_=100,
            position="right",
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#91CC75")),
            axislabel_opts=opts.LabelOpts(formatter="{value}%"),
        )
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="中国网民规模与互联网普及率变化（2010-2025）",
                                  subtitle="数据来源：CNNIC 中国互联网络发展状况统计报告"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="网民规模（亿）", min_=0,
                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿")),
        legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
    )
    line = Line()
    line.add_xaxis(years)
    line.add_yaxis(
        "互联网普及率（%）", penetration,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=True, formatter="{c}%"),
        linestyle_opts=opts.LineStyleOpts(width=3, color="#91CC75"),
        itemstyle_opts=opts.ItemStyleOpts(color="#91CC75"),
        areastyle_opts=opts.AreaStyleOpts(opacity=0.15, color="#91CC75"),
    )
    bar.overlap(line)
    return bar


def make_chart2():
    line = Line(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart2"
    ))
    line.add_xaxis(years)
    line.add_yaxis(
        "手机网民规模（亿）", mobile_users,
        label_opts=opts.LabelOpts(is_show=True, formatter="{c}亿"),
        linestyle_opts=opts.LineStyleOpts(width=3, color="#5470C6"),
        symbol="circle",
        symbol_size=10,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.2, color="#5470C6"),
    )
    line.add_yaxis(
        "手机网民占比（%）", mobile_pct,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=True, formatter="{c}%"),
        linestyle_opts=opts.LineStyleOpts(width=3, color="#EE6666", type_="dashed"),
        symbol="diamond",
        symbol_size=10,
    )
    line.extend_axis(
        yaxis=opts.AxisOpts(
            name="手机网民占比（%）",
            type_="value",
            min_=60,
            max_=100,
            position="right",
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#EE6666")),
            axislabel_opts=opts.LabelOpts(formatter="{value}%"),
        )
    )
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="中国手机网民规模及占比变化（2010-2025）"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="手机网民规模（亿）",
                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿")),
        legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
    )
    return line


def make_chart3():
    age_groups = list(df_age.columns[1:])
    bar = Bar(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart3"
    ))
    bar.add_xaxis(df_age["年份"].astype(str).tolist())
    colors = ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE", "#3BA272", "#FC8452"]
    for i, group in enumerate(age_groups):
        vals = df_age[group].tolist()
        bar.add_yaxis(
            group, vals,
            stack="age",
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color=colors[i % len(colors)]),
        )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="中国网民年龄结构演变（2013-2024）"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow",
                                       formatter=JsCode("""
            function(params) {
                let total = 0;
                params.forEach(p => { total += p.data; });
                let html = params[0].axisValue + '<br/>';
                params.forEach(p => {
                    let pct = (p.data / total * 100).toFixed(1);
                    html += p.marker + ' ' + p.seriesName + ': ' + p.data + '%<br/>';
                });
                return html;
            }
        """)),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="占比（%）",
                                  axislabel_opts=opts.LabelOpts(formatter="{value}%")),
        legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom", orient="horizontal"),
    )
    return bar


def make_chart4():
    edu_groups = list(df_edu.columns[1:])
    last_row = df_edu.iloc[-1]
    pie = Pie(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart4"
    ))
    data_pairs = [(group, last_row[group]) for group in edu_groups]
    pie.add(
        "", data_pairs,
        radius=["35%", "60%"],
        center=["50%", "55%"],
        label_opts=opts.LabelOpts(
            is_show=True,
            formatter="{b}: {d}%",
            font_size=13,
        ),
        itemstyle_opts=opts.ItemStyleOpts(
            border_color="#fff", border_width=2
        ),
    )
    pie.set_global_opts(
        title_opts=opts.TitleOpts(
            title="2024年中国网民学历结构分布",
            subtitle="环比分析见报告正文",
            pos_left="center",
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_left="left",
            pos_top="center",
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}: {c}% ({d}%)",
        ),
    )
    return pie


def make_chart5():
    df_sorted = df_app.sort_values("用户规模_亿", ascending=True)
    bar = Bar(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart5"
    ))
    bar.add_xaxis(df_sorted["应用类别"].tolist())
    bar.add_yaxis(
        "用户规模（亿）", df_sorted["用户规模_亿"].tolist(),
        label_opts=opts.LabelOpts(is_show=True, position="right",
                                   formatter="{c}亿"),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode("""
                new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                    {offset: 0, color: '#5470C6'},
                    {offset: 1, color: '#91CC75'}
                ])
            """)
        ),
    )
    bar.reversal_axis()
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="2024年中国主要互联网应用用户规模排名"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        xaxis_opts=opts.AxisOpts(name="用户规模（亿）",
                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿")),
        yaxis_opts=opts.AxisOpts(name="应用类别"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    return bar


def make_chart6():
    bar = Bar(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart6"
    ))
    bar.add_xaxis(df_ip["年份"].astype(str).tolist())
    bar.add_yaxis(
        "IPv4地址（亿）", df_ip["IPv4_亿"].tolist(),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
        itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),
    )
    bar.add_yaxis(
        "IPv6地址（亿）", df_ip["IPv6_亿"].tolist(),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
        itemstyle_opts=opts.ItemStyleOpts(color="#91CC75"),
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="中国IPv4/IPv6地址资源变化（2017-2024）"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="地址数量（亿）",
                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿")),
        legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
    )
    return bar


def make_chart7():
    bar = Bar(init_opts=opts.InitOpts(
        width="1200px", height="600px",
        theme=ThemeType.LIGHT,
        chart_id="chart7"
    ))
    bar.add_xaxis(df_ur["年份"].astype(str).tolist())
    bar.add_yaxis(
        "城镇普及率（%）", df_ur["城镇普及率_百分比"].tolist(),
        label_opts=opts.LabelOpts(is_show=True, position="top", formatter="{c}%"),
        itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),
    )
    bar.add_yaxis(
        "农村普及率（%）", df_ur["农村普及率_百分比"].tolist(),
        label_opts=opts.LabelOpts(is_show=True, position="top", formatter="{c}%"),
        itemstyle_opts=opts.ItemStyleOpts(color="#91CC75"),
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="中国城乡互联网普及率对比（2013-2024）"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="普及率（%）",
                                  axislabel_opts=opts.LabelOpts(formatter="{value}%")),
        legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
    )
    return bar


def main():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        make_chart1(),
        make_chart2(),
        make_chart3(),
        make_chart4(),
        make_chart5(),
        make_chart7(),
        make_chart6(),
    )
    out_path = os.path.join(OUT_DIR, "visualization.html")
    page.render(out_path)
    print(f"All charts saved to: {out_path}")


if __name__ == "__main__":
    main()
