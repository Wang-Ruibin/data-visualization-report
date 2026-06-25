# 📊 中国互联网发展态势可视化分析 (2010–2025)

基于 CNNIC 历年《中国互联网络发展状况统计报告》数据，使用 **Python + PyECharts** 对中国互联网发展态势进行可视化分析。

## ✨ 效果预览

| 图表 | 说明 |
|------|------|
| ![chart1](https://img.shields.io/badge/Chart-1-blue) | 网民规模与互联网普及率变化（柱线组合图） |
| ![chart2](https://img.shields.io/badge/Chart-2-green) | 手机网民规模及占比变化（双轴折线图） |
| ![chart3](https://img.shields.io/badge/Chart-3-orange) | 网民年龄结构演变（堆叠柱状图） |
| ![chart4](https://img.shields.io/badge/Chart-4-red) | 2024年网民学历结构分布（环形图） |
| ![chart5](https://img.shields.io/badge/Chart-5-purple) | 主要互联网应用用户规模排名（横向柱状图） |
| ![chart6](https://img.shields.io/badge/Chart-6-teal) | IPv4/IPv6 地址资源变化（分组柱状图） |
| ![chart7](https://img.shields.io/badge/Chart-7-cyan) | 城乡互联网普及率对比（分组柱状图） |

> 所有图表可在 `code/visualization.html` 中交互查看（悬浮、缩放、图例筛选）。

## 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/2308080119/data-visualization-report.git
cd data-visualization-report

# 2. 安装依赖
pip install pyecharts pandas

# 3. 运行可视化脚本
cd code
python3 visualization.py
```

浏览器打开 `code/visualization.html` 即可查看交互式图表。

## 📁 目录结构

```
.
├── data/              # 原始数据集（CSV）
│   ├── internet_users.csv    # 网民规模与普及率
│   ├── age_structure.csv     # 年龄结构
│   ├── education_structure.csv # 学历结构
│   ├── app_users.csv         # 应用用户规模
│   ├── urban_rural.csv       # 城乡普及率
│   └── ip_addresses.csv      # IP地址资源
├── code/              # 可视化源码
│   ├── visualization.py     # PyECharts 绘图脚本
│   └── visualization.html   # 生成的交互式图表
├── report/            # 课程报告（Word）
└── README.md
```

## 🛠️ 技术栈

- **Python 3** — 数据处理
- **Pandas** — 数据读取与清洗
- **PyECharts** — 交互式可视化
- **CNNIC** — 数据来源

## 📜 数据来源

中国互联网络信息中心（CNNIC）《中国互联网络发展状况统计报告》
- 第 47–55 次《中国互联网络发展状况统计报告》
- 覆盖时间范围：2010–2025 年

## 📄 许可

本项目仅用于课程学习目的。

---

⭐ **如果你觉得这个项目还不错，给我一个 Star 吧～ 你的鼓励是开源路上最好的燃料！** 🚀🌟
