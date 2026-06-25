import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
IMG_DIR = os.path.join(BASE_DIR, "..", "report", "images")
os.makedirs(IMG_DIR, exist_ok=True)

plt.rcParams['axes.unicode_minus'] = False

font_names = [
    'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC',
    'Noto Sans SC', 'Source Han Sans SC', 'SimHei', 'Microsoft YaHei',
    'DejaVu Sans',
]
available_font = None
for fn in font_names:
    try:
        fm.findfont(fn, fallback_to_default=False)
        available_font = fn
        break
    except Exception:
        continue

if available_font:
    plt.rcParams['font.family'] = available_font
    print(f"Using font: {available_font}")
else:
    print("No CJK font found, installing...")
    import subprocess
    subprocess.run(["fc-cache", "-f"], capture_output=True)
    for fn in font_names:
        try:
            fm.findfont(fn, fallback_to_default=False)
            available_font = fn
            break
        except Exception:
            continue
    if available_font:
        plt.rcParams['font.family'] = available_font
        print(f"Using font: {available_font}")
    else:
        print("WARNING: No CJK font found, Chinese text may not display")

WEBSITE = "数据来源：CNNIC 中国互联网络发展状况统计报告"

def save(fig, name):
    path = os.path.join(IMG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {path}")
    return path


# Chart 1
def make_chart1():
    df = pd.read_csv(os.path.join(DATA_DIR, "internet_users.csv"))
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.bar(df["年份"], df["网民规模_亿"], color='#5470C6', alpha=0.85, width=0.6, label='网民规模（亿）')
    for x, y in zip(df["年份"], df["网民规模_亿"]):
        ax1.text(x, y + 0.15, f'{y}', ha='center', va='bottom', fontsize=8, color='#5470C6')
    ax1.set_xlabel('年份')
    ax1.set_ylabel('网民规模（亿）', color='#5470C6')
    ax1.tick_params(axis='y', labelcolor='#5470C6')
    ax2 = ax1.twinx()
    ax2.plot(df["年份"], df["互联网普及率_百分比"], color='#91CC75', marker='o', linewidth=2.5, label='互联网普及率（%）')
    ax2.fill_between(df["年份"], df["互联网普及率_百分比"], alpha=0.12, color='#91CC75')
    for x, y in zip(df["年份"], df["互联网普及率_百分比"]):
        ax2.text(x, y + 1.2, f'{y}%', ha='center', va='bottom', fontsize=8, color='#91CC75')
    ax2.set_ylabel('互联网普及率（%）', color='#91CC75')
    ax2.tick_params(axis='y', labelcolor='#91CC75')
    ax1.set_title('中国网民规模与互联网普及率变化（2010-2025）', fontsize=14, fontweight='bold')
    fig.text(0.5, -0.02, WEBSITE, ha='center', fontsize=9, color='gray')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    fig.tight_layout()
    return save(fig, "chart1_users_penetration.png")


# Chart 2
def make_chart2():
    df = pd.read_csv(os.path.join(DATA_DIR, "internet_users.csv"))
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(df["年份"], df["手机网民_亿"], color='#5470C6', marker='o', linewidth=2.5, label='手机网民规模（亿）')
    ax1.fill_between(df["年份"], df["手机网民_亿"], alpha=0.15, color='#5470C6')
    for x, y in zip(df["年份"], df["手机网民_亿"]):
        ax1.text(x, y + 0.15, f'{y}亿', ha='center', va='bottom', fontsize=8, color='#5470C6')
    ax1.set_xlabel('年份')
    ax1.set_ylabel('手机网民规模（亿）', color='#5470C6')
    ax1.tick_params(axis='y', labelcolor='#5470C6')
    ax2 = ax1.twinx()
    ax2.plot(df["年份"], df["手机网民占比_百分比"], color='#EE6666', marker='D', linewidth=2.5, linestyle='--', label='手机网民占比（%）')
    for x, y in zip(df["年份"], df["手机网民占比_百分比"]):
        ax2.text(x, y + 0.8, f'{y}%', ha='center', va='bottom', fontsize=8, color='#EE6666')
    ax2.set_ylabel('手机网民占比（%）', color='#EE6666')
    ax2.tick_params(axis='y', labelcolor='#EE6666')
    ax1.set_title('中国手机网民规模及占比变化（2010-2025）', fontsize=14, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    fig.tight_layout()
    return save(fig, "chart2_mobile.png")


# Chart 3
def make_chart3():
    df = pd.read_csv(os.path.join(DATA_DIR, "age_structure.csv"))
    colors = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE', '#3BA272', '#FC8452']
    fig, ax = plt.subplots(figsize=(12, 5))
    x = df["年份"].astype(str)
    groups = list(df.columns[1:])
    bottom = np.zeros(len(df))
    for i, g in enumerate(groups):
        vals = df[g].values
        ax.bar(x, vals, bottom=bottom, label=g, color=colors[i % len(colors)], width=0.6)
        bottom += vals
    ax.set_xlabel('年份')
    ax.set_ylabel('占比（%）')
    ax.set_title('中国网民年龄结构演变（2013-2024）', fontsize=14, fontweight='bold')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=4, fontsize=9)
    fig.tight_layout()
    return save(fig, "chart3_age.png")


# Chart 4
def make_chart4():
    df = pd.read_csv(os.path.join(DATA_DIR, "education_structure.csv"))
    last = df.iloc[-1]
    groups = list(df.columns[1:])
    vals = [last[g] for g in groups]
    colors = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE']
    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(
        vals, labels=groups, autopct='%1.1f%%',
        colors=colors, startangle=90, pctdistance=0.75,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        textprops={'fontsize': 11},
    )
    plt.setp(autotexts, size=10, weight='bold', color='white')
    ax.set_title('2024年中国网民学历结构分布', fontsize=14, fontweight='bold', pad=20)
    centre = plt.Circle((0, 0), 0.45, fc='white')
    fig.gca().add_artist(centre)
    fig.tight_layout()
    return save(fig, "chart4_education.png")


# Chart 5
def make_chart5():
    df = pd.read_csv(os.path.join(DATA_DIR, "app_users.csv")).sort_values("用户规模_亿")
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.barh(df["应用类别"], df["用户规模_亿"], color='#5470C6', alpha=0.85, height=0.6)
    for bar, v in zip(bars, df["用户规模_亿"]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{v}亿',
                va='center', fontsize=9, color='#5470C6')
    ax.set_xlabel('用户规模（亿）')
    ax.set_ylabel('应用类别')
    ax.set_title('2024年中国主要互联网应用用户规模排名', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    fig.tight_layout()
    return save(fig, "chart5_apps.png")


# Chart 6
def make_chart6():
    df = pd.read_csv(os.path.join(DATA_DIR, "urban_rural.csv"))
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    w = 0.35
    bars1 = ax.bar(x - w/2, df["城镇普及率_百分比"], w, label='城镇普及率（%）', color='#5470C6', alpha=0.9)
    bars2 = ax.bar(x + w/2, df["农村普及率_百分比"], w, label='农村普及率（%）', color='#91CC75', alpha=0.9)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.0f}%',
                ha='center', va='bottom', fontsize=9, color='#5470C6')
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.0f}%',
                ha='center', va='bottom', fontsize=9, color='#91CC75')
    ax.set_xticks(x)
    ax.set_xticklabels(df["年份"].astype(str))
    ax.set_xlabel('年份')
    ax.set_ylabel('普及率（%）')
    ax.set_title('中国城乡互联网普及率对比（2013-2024）', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    fig.tight_layout()
    return save(fig, "chart6_urban_rural.png")


# Chart 7
def make_chart7():
    df = pd.read_csv(os.path.join(DATA_DIR, "ip_addresses.csv"))
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    w = 0.35
    bars1 = ax.bar(x - w/2, df["IPv4_亿"], w, label='IPv4地址（亿）', color='#5470C6', alpha=0.9)
    bars2 = ax.bar(x + w/2, df["IPv6_亿"], w, label='IPv6地址（亿）', color='#91CC75', alpha=0.9)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f'{bar.get_height():.2f}',
                ha='center', va='bottom', fontsize=8, color='#5470C6')
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f'{bar.get_height():.2f}',
                ha='center', va='bottom', fontsize=8, color='#91CC75')
    ax.set_xticks(x)
    ax.set_xticklabels(df["年份"].astype(str))
    ax.set_xlabel('年份')
    ax.set_ylabel('地址数量（亿）')
    ax.set_title('中国IPv4/IPv6地址资源变化（2017-2024）', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    fig.tight_layout()
    return save(fig, "chart7_ip.png")


def main():
    print("Generating chart images for report...")
    images = {}
    images['chart1'] = make_chart1()
    images['chart2'] = make_chart2()
    images['chart3'] = make_chart3()
    images['chart4'] = make_chart4()
    images['chart5'] = make_chart5()
    images['chart6'] = make_chart6()
    images['chart7'] = make_chart7()
    print(f"\nAll {len(images)} chart images saved to {IMG_DIR}/")


if __name__ == "__main__":
    main()
