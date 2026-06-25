from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "..", "report", "images")
REPORT_DIR = os.path.join(BASE_DIR, "..", "report")
os.makedirs(REPORT_DIR, exist_ok=True)

doc = Document()

FONT_BODY = '宋体'
FONT_HEADING = '黑体'
FONT_EN = 'Times New Roman'

style = doc.styles['Normal']
style.font.name = FONT_BODY
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.first_line_indent = Cm(0.74)


def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.font.name = FONT_HEADING
        run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_HEADING)
    return h


def add_para(text, bold=False, align=None, indent=True, size=Pt(12)):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74) if indent else Cm(0)
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.font.name = FONT_BODY
    run.font.size = size
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)
    if bold:
        run.bold = True
    return p


def add_chart(image_path, caption, width=Inches(5.5)):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(image_path, width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = Cm(0)
    cap.paragraph_format.space_before = Pt(4)
    cap.paragraph_format.space_after = Pt(8)
    run = cap.add_run(caption)
    run.font.size = Pt(10)
    run.font.name = FONT_BODY
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)
    run.italic = True


img = lambda name: os.path.join(IMG_DIR, name)

# ====== Title Page ======
for _ in range(3):
    doc.add_paragraph()

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title_p.add_run("《数据可视化技术》课程报告")
run.font.size = Pt(26)
run.bold = True
run.font.name = FONT_HEADING
run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_HEADING)

doc.add_paragraph()

subtitle_p = doc.add_paragraph()
subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle_p.add_run("中国互联网发展态势可视化分析\n（2010–2025）")
run.font.size = Pt(18)
run.font.name = FONT_HEADING
run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_HEADING)

for _ in range(5):
    doc.add_paragraph()

info_items = [
    ("学    院", "商学院"),
    ("专    业", "信息管理与信息系统"),
    ("学    号", "2308080119"),
    ("姓    名", "王睿彬"),
    ("课    程", "数据可视化技术"),
    ("学    期", "2025–2026学年第二学期"),
]
for label, value in info_items:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(f"{label}：{value}")
    run.font.size = Pt(15)
    run.font.name = FONT_BODY
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

doc.add_page_break()

# ====== 正文 ======

add_heading_styled("一、引言", level=1)

add_para(
    "从2010年到今天，中国互联网经历了一场深刻的变革。"
    "还记得2010年那会儿，3G网络刚刚普及不久，智能手机还是个新鲜玩意儿，"
    "上网主要还得靠电脑。而现在，人手一部手机就能搞定几乎所有事情——"
    "聊天、购物、看视频、点外卖、交水电费，互联网已经完全融入了我们的日常生活。"
)

add_para(
    "这十几年，中国互联网到底发生了哪些变化？网民有多少？"
    "大家都是用什么设备上网的？上网的人都是什么年龄、什么学历？"
    "城市和农村的差距大不大？这些问题如果能用数据回答，应该很有意思。"
)

add_para(
    "正好，中国互联网络信息中心（CNNIC）每半年发布一次"
    "《中国互联网络发展状况统计报告》，里面记录了各种各样的互联网指标数据。"
    "我这篇报告就是把这些数据整理出来，用图表的形式展示给大家看。"
    "数据跨度从2010年到2025年，涵盖了网民规模、普及率、用户结构、应用发展等多个方面。"
)

add_para(
    "在可视化工具方面，我选了PyECharts和Matplotlib。"
    "PyECharts生成的是交互式网页图表，可以用鼠标悬浮看数据、缩放、筛选，"
    "很适合在电脑上直接浏览。报告中放的静态图是用Matplotlib画的，方便打印阅读。"
    "两种图表搭配着来，各有各的优势。"
)

add_heading_styled("二、数据来源与处理", level=1)

add_para(
    "数据来自CNNIC第27次到第55次《中国互联网络发展状况统计报告》，"
    "时间跨度2010年至2025年。具体包括以下几个数据集："
)

items = [
    "网民规模与互联网普及率（2010–2025，逐年）",
    "手机网民规模及占比（2010–2025，逐年）",
    "网民年龄结构（2013、2016、2019、2022、2024）",
    "网民学历结构（2013、2016、2019、2022、2024）",
    "各类互联网应用用户规模（2024年）",
    "城镇、农村互联网普及率对比（2013、2016、2019、2022、2024）",
    "IPv4/IPv6地址资源数量（2017–2024，逐年）",
]
for item in items:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(item)
    run.font.size = Pt(12)
    run.font.name = FONT_BODY
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

add_para(
    "数据整理过程比较简单：从CNNIC报告原文里把数字提取出来，存成CSV格式，"
    "然后用Pandas库读进来处理。年份不连续的那些指标（比如年龄结构），"
    "我就直接用了手头有的年份数据，没有做插值或者推算，保证每个数字都是报告里写的原数。"
)

add_heading_styled("三、可视化分析与发现", level=1)

add_heading_styled("3.1 网民规模和普及率——从4.5亿到11亿的飞跃", level=2)

add_para(
    "先看一张总体情况的图。"
)

add_chart(img("chart1_users_penetration.png"),
          "图1 中国网民规模与互联网普及率变化（2010-2025）")

add_para(
    "从图1可以很直观地看到，中国网民规模从2010年的4.57亿一路涨到了2025年的11.25亿，"
    "十五年翻了一倍多。普及率也从34.3%提高到了79.8%，"
    "也就是说现在将近八成中国人都在上网。"
)

add_para(
    "细看增长曲线的话，会发现前十年（2010–2020）增长特别猛，"
    "基本上每年新增四五千万网民。这段时间正好赶上了3G普及、4G爆发、"
    "智能手机价格打到千元以下，上网的门槛一下子降了很多。"
    "2020年以后增速明显慢下来了，一年也就新增两三千万人——"
    "这也正常，毕竟能上网的人大部分都已经上了，市场饱和了嘛。"
)

add_heading_styled("3.2 手机网民——从配角到绝对主角", level=2)

add_chart(img("chart2_mobile.png"),
          "图2 中国手机网民规模及占比变化（2010-2025）")

add_para(
    "图2讲的是手机上网的情况。2010年的时候，虽然有手机网民这个概念，"
    "但占比才66.2%，也就是说还有三分之一的人是用电脑或者其他设备上网的。"
    "而到了2025年，手机网民占比已经达到了99.9%，基本上等于所有人都在用手机上网了。"
)

add_para(
    "转折点出现在2015年——那一年手机网民占比首次突破90%。"
    "从那以后，桌面端的地位就越来越边缘化了。"
    "现在做个互联网产品要是没有手机版，基本等于放弃市场。"
    "这种变化也在很大程度上塑造了中国互联网的生态——"
    "为什么中国的移动支付、短视频、外卖能做得这么好？"
    "很大程度上就是因为大家都是手机上网，这些服务天然就有用户基础。"
)

add_heading_styled("3.3 年龄结构——互联网不再只是年轻人的事", level=2)

add_chart(img("chart3_age.png"),
          "图3 中国网民年龄结构演变（2013-2024）")

add_para(
    "图3的堆叠柱状图展示了不同年龄段网民占比的变化。这个图挺有意思的。"
)

add_para(
    "最大的变化在中老年群体。2013年，50岁以上的网民加一起才占7.6%，"
    "几乎可以忽略不计。但到了2024年，这个比例涨到了22.8%，"
    "特别是60岁以上的老年网民，从2.5%涨到了7.6%。"
    "你身边的长辈是不是这几年也开始刷短视频、用微信发红包了？数据正好说明了这个趋势。"
)

add_para(
    "年轻网民的比例则是在下降的。20-29岁从31.2%降到了18.7%，"
    "降了将近13个百分点。不过这不代表年轻人不上网了，"
    '而是因为中老年群体大量涌入，把占比"稀释"了。'
    "实际上年轻网民的上网时长和活跃度还是最高的。"
)

add_heading_styled("3.4 学历结构——各学历层次分布相对均匀", level=2)

add_chart(img("chart4_education.png"),
          "图4 2024年中国网民学历结构分布")

add_para(
    "图4是2024年的学历结构环形图。初中占比最大（32.8%），"
    "高中/中专和大专/本科各占26.2%和27.6%，三者比较接近。"
    "小学及以下占8.8%，硕士以上占4.6%。整体来看分布还是比较均匀的。"
)

add_para(
    "这几年高学历网民的比例在稳步提升。大专/本科及以上占比"
    "从2013年的20.9%涨到了2024年的32.2%，说明越来越多受过高等教育的人在上网。"
    "不过低学历群体的绝对规模还是很大，所以互联网产品在设计上"
    "需要考虑不同教育背景用户的使用习惯——不是所有用户都能看懂复杂的操作。"
)

add_heading_styled("3.5 互联网应用——即时通信和视频是两大霸主", level=2)

add_chart(img("chart5_apps.png"),
          "图5 2024年中国主要互联网应用用户规模排名")

add_para(
    "图5是2024年各类互联网应用的用户规模排行。不出意外，即时通信排第一，"
    "10.7亿用户——微信和QQ几乎覆盖了所有网民。"
    "网络视频（含短视频）以10.5亿排第二，"
    "抖音、快手这些短视频平台功不可没。"
)

add_para(
    "网络支付9.8亿排第三，这个数字挺惊人的——"
    "基本上是个网民就会用移动支付。"
    "搜索引擎（8.9亿）和网络购物（8.7亿）分列四、五位，"
    "都是国民级应用了。"
)

add_para(
    "比较有意思的是在线教育（4.2亿）和在线办公（5.3亿），"
    "这两个在2020年疫情期间经历了一波暴涨，"
    "疫情之后虽然有所回落，但用户规模还是比疫情前大了不少。"
    "说明有些习惯一旦养成就回不去了。"
)

add_heading_styled("3.6 城乡差距——进步很大，差距仍在", level=2)

add_chart(img("chart6_urban_rural.png"),
          "图6 中国城乡互联网普及率对比（2013-2024）")

add_para(
    "图6对比了城镇和农村的互联网普及率。城镇从2013年的62.0%涨到了2024年的84.5%，"
    "农村从28.1%涨到了65.3%。虽然农村的绝对水平还赶不上城镇，"
    "但增长速度明显更快——十年间从28%涨到65%，涨幅超过130%。"
)

add_para(
    "城乡之间的差距从2013年的34个百分点缩小到了2024年的19个百分点，"
    '说明"数字鸿沟"在逐渐收窄，但19个百分点的差距还是不小。'
    "这背后涉及到网络基础设施、经济水平、教育程度等多方面因素。"
    '这几年国家推的"宽带中国"和电信普遍服务确实起了作用，'
    "但想让农村和城镇完全拉平，还需要时间。"
)

add_heading_styled("3.7 IPv4/IPv6地址——IPv6正在加速追赶", level=2)

add_chart(img("chart7_ip.png"),
          "图7 中国IPv4/IPv6地址资源变化（2017-2024）")

add_para(
    "最后一个图表讲的是IP地址资源。IPv4地址这几年几乎没怎么涨——"
    "从3.39亿到3.62亿，主要是因为IPv4地址早就分配完了，"
    "全球就那么几个，用完了就没有了。"
)

add_para(
    "IPv6就完全是另一番景象了。从2017年的0.86亿一路涨到了2024年的2.63亿，"
    "翻了将近三倍。这跟国家的推动有很大关系——"
    "2017年国家发了文件专门部署IPv6的规模部署，"
    "运营商和互联网企业都在积极响应。"
    "现在中国的IPv6活跃用户数在全球都是排在前面的。"
    "未来IPv6全面取代IPv4应该是大势所趋。"
)

add_heading_styled("四、总结", level=1)

add_para(
    "回顾2010年到2025年中国互联网这十五年的发展，有几个很明显的趋势："
)

conclusions = [
    "规模大，但增长放缓了。网民从4.57亿涨到11.25亿，普及率接近八成，"
    "但增量红利基本见顶，以后更多是存量竞争。",

    "手机是绝对的主流。手机网民占比超过99.9%，"
    "做互联网服务不考虑移动端基本等于没做。",

    "用户越来越多元。老人和小孩都在上网，学历分布也越来越均匀，"
    "互联网服务需要考虑不同群体的需求。",

    "城乡差距在缩小，但还需要继续努力。农村普及率十年翻了一番多，"
    "但跟城镇比还有差不多20个百分点的差距。",

    "基础设施在升级。IPv6的快速部署为互联网的长期发展打好了基础。",

    "应用生态丰富多样。从聊天、购物到看视频、办公，"
    "互联网已经渗透到了生活的每个角落。",
]
for c in conclusions:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(f"• {c}")
    run.font.size = Pt(12)
    run.font.name = FONT_BODY
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

add_para(
    "最后说一句，做这个报告的过程本身也挺有收获的。"
    "以前看CNNIC的报告觉得就是一堆数字，"
    "但真正动手把数据整理成图表之后，很多趋势就一目了然了。"
    '数据可视化确实是个好工具，能让数据自己"说话"。'
)

add_heading_styled("参考文献", level=1)

refs = [
    "[1] 中国互联网络信息中心. 第27次中国互联网络发展状况统计报告[R]. 北京, 2010.",
    "[2] 中国互联网络信息中心. 第37次中国互联网络发展状况统计报告[R]. 北京, 2015.",
    "[3] 中国互联网络信息中心. 第47次中国互联网络发展状况统计报告[R]. 北京, 2020.",
    "[4] 中国互联网络信息中心. 第51次中国互联网络发展状况统计报告[R]. 北京, 2022.",
    "[5] 中国互联网络信息中心. 第53次中国互联网络发展状况统计报告[R]. 北京, 2023.",
    "[6] 中国互联网络信息中心. 第55次中国互联网络发展状况统计报告[R]. 北京, 2024.",
    "[7] 中共中央办公厅, 国务院办公厅. 推进互联网协议第六版（IPv6）规模部署行动计划[Z]. 2017.",
]
for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(ref)
    run.font.size = Pt(11)
    run.font.name = FONT_BODY
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

out_path = os.path.join(REPORT_DIR, "2308080119+王睿彬+数据源码.docx")
doc.save(out_path)
print(f"Report saved to: {out_path}")
