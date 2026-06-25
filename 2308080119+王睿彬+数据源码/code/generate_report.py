from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "..", "report", "images")
REPORT_DIR = os.path.join(BASE_DIR, "..", "report")
os.makedirs(REPORT_DIR, exist_ok=True)

doc = Document()

FONT_BODY = '宋体'
FONT_HEADING = '黑体'

style = doc.styles['Normal']
style.font.name = FONT_BODY
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.first_line_indent = Cm(0.74)

def set_font(run, name, size):
    run.font.name = name
    run.font.size = size
    run.element.rPr.rFonts.set(qn('w:eastAsia'), name)

def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.first_line_indent = Cm(0)
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
    set_font(run, FONT_BODY, size)
    if bold:
        run.bold = True
    return p

def add_chart(image_path, caption, width=Inches(5.2)):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run()
    run.add_picture(image_path, width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = Cm(0)
    cap.paragraph_format.space_before = Pt(2)
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
title_p.paragraph_format.first_line_indent = Cm(0)
run = title_p.add_run("《数据可视化技术》课程报告")
run.font.size = Pt(26)
run.bold = True
run.font.name = FONT_HEADING
run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_HEADING)

doc.add_paragraph()

subtitle_p = doc.add_paragraph()
subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle_p.paragraph_format.first_line_indent = Cm(0)
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

from docx.shared import Emu
from docx.oxml import OxmlElement
from docx.enum.table import WD_TABLE_ALIGNMENT

def remove_cell_margins(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for side in ['top', 'left', 'bottom', 'right']:
        mar = OxmlElement(f'w:{side}')
        mar.set(qn('w:w'), '0')
        mar.set(qn('w:type'), 'dxa')
        tcMar.append(mar)
    tcPr.append(tcMar)

table = doc.add_table(rows=6, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
for row_idx, (label, value) in enumerate(info_items):
    row = table.rows[row_idx]
    row.height = Cm(0.9)

    cell0 = row.cells[0]
    cell0.width = Cm(3.2)
    remove_cell_margins(cell0)
    cell0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    cell0.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
    cell0.paragraphs[0].paragraph_format.space_before = Pt(0)
    cell0.paragraphs[0].paragraph_format.space_after = Pt(0)
    run0 = cell0.paragraphs[0].add_run(f"{label}：")
    run0.font.size = Pt(15)
    run0.font.name = FONT_BODY
    run0.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

    cell1 = row.cells[1]
    cell1.width = Cm(8)
    remove_cell_margins(cell1)
    cell1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell1.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
    cell1.paragraphs[0].paragraph_format.space_before = Pt(0)
    cell1.paragraphs[0].paragraph_format.space_after = Pt(0)
    run1 = cell1.paragraphs[0].add_run(value)
    run1.font.size = Pt(15)
    run1.font.name = FONT_BODY
    run1.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

    tc = cell1._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), '000000')
    tcBorders.append(bottom)
    tcPr.append(tcBorders)

for row in table.rows:
    for cell in row.cells:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = tcPr.find(qn('w:tcBorders'))
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
        for side in ['top', 'left', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'none')
            border.set(qn('w:sz'), '0')
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), 'auto')
            tcBorders.append(border)
        tcPr.append(tcBorders)

doc.add_page_break()

# ====== 正文 ======

add_heading_styled("一、引言", level=1)

add_para(
    "从2010年到现在，中国互联网的变化真的太大了。"
    "2010年那会儿3G刚普及，智能手机还是个贵东西，上网主要是用电脑。"
    "现在呢，一部手机什么都搞定了——聊天、买东西、看视频、点外卖、交水电费。"
    "我很好奇这十几年这些变化到底有多大，所以找了CNNIC的数据来做这个分析。"
)

add_para(
    "CNNIC每半年发一次《中国互联网络发展状况统计报告》，里面有各种互联网指标。"
    "我把2010到2025年的关键数据整理出来，画成图表。"
    "主要看网民有多少、普及率多高、用手机上网的比例、"
    "上网的人是什么年龄和学历、大家都在用什么应用、"
    "城乡差距怎么样、还有IP地址的变化。"
)

add_para(
    "工具用的是PyECharts和Matplotlib。"
    "PyECharts可以生成交互式网页图表，用浏览器打开能悬停看数据、缩放什么的。"
    "Matplotlib画的图放在报告里，方便打印。"
)

add_heading_styled("二、数据来源与处理", level=1)

add_para(
    "数据全部来自CNNIC第27次到第55次报告（2010-2025年）。"
    "总共整理成七个CSV文件，分别对应网民规模与普及率、手机网民、"
    "年龄结构、学历结构、应用用户规模、城乡普及率和IP地址资源。"
    "有些指标不是每年都有数据，比如年龄结构只有几个年份的，"
    "我就直接用了这些年份，没做插值，保证数字都是原始值。"
)

add_heading_styled("三、可视化分析与发现", level=1)

add_heading_styled("3.1 网民规模和普及率", level=2)

add_chart(img("chart1_users_penetration.png"),
          "图1 中国网民规模与互联网普及率变化（2010-2025）")

add_para(
    "这张图用了柱线组合——柱线组合能把两个量纲不同的指标放一起，柱子看绝对规模，折线看变化趋势。"
    "CNNIC的数据显示，网民从2010年的4.57亿涨到了2025年的11.25亿，翻了不止一倍。"
    "普及率也从34.3%到了79.8%，快八成人都在上网了。"
)

add_para(
    "前十年涨得特别快，每年基本能多四五千万人。"
    "那段时间正好3G变4G、智能手机也越来越便宜，上网的门槛降了很多。"
    "2020年后增速慢了，一年就多两三千万——"
    "其实想想也正常，该上的都上了，哪来那么多人。"
)

add_heading_styled("3.2 手机网民", level=2)

add_chart(img("chart2_mobile.png"),
          "图2 中国手机网民规模及占比变化（2010-2025）")

add_para(
    "这个有意思。双轴折线图左边是手机网民规模、右边是占比，"
    "两个量纲不一样但放在一起看还挺清楚。"
    "2010年手机上网的比例才66.2%，"
    "就是说那时候还有三分之一的人是用电脑上网的。"
    "到了2025年，这个数字到了99.9%，基本等于全民手机上网了。"
)

add_para(
    "转折点是2015年，那一年手机占比第一次超过90%。"
    "从那以后，电脑上网的人越来越少。"
    "想想也是，现在谁还专门开电脑上个网啊，手机多方便。"
    "移动支付、短视频、外卖这些能在中国发展得这么好，"
    "跟全民手机上网有很大关系。"
)

add_heading_styled("3.3 年龄结构", level=2)

add_chart(img("chart3_age.png"),
          "图3 中国网民年龄结构演变（2013-2024）")

add_para(
    "堆叠柱状图可以看到不同年龄段的组成变化。"
    "最大的变化在中老年。2013年50岁以上的网民加起来才7.6%，"
    "2024年变到了22.8%。60岁以上的从2.5%涨到7.6%。"
    "想想身边的长辈，是不是也开始刷短视频、发微信红包了？数据也这么说。"
)

add_para(
    "年轻人比例反而降了。20到29岁的从31.2%降到18.7%，"
    "不过这应该不是年轻人不上网了，而是老年人进来多了被稀释了。"
    "30到39岁一直比较稳定，在20%到24%之间，"
    "40到49岁从12.5%涨到21.5%，说明上网的人群确实在往高龄走。"
)

add_heading_styled("3.4 学历结构", level=2)

add_chart(img("chart4_education.png"),
          "图4 2024年中国网民学历结构分布")

add_para(
    "学历是分类变量，用环形图看占比比较直观。"
    "初中学历最多（32.8%），高中/中专和大专/本科各占26.2%和27.6%，差不太多。"
    "小学及以下8.8%，硕士以上4.6%。"
    "高学历的比例在慢慢涨，大专及以上从2013年的20.9%到了2024年的32.2%。"
    "不过低学历的人还是很多，做互联网产品的人得考虑到这一点，"
    "不是所有人都能看懂复杂的界面。"
)

add_heading_styled("3.5 互联网应用", level=2)

add_chart(img("chart5_apps.png"),
          "图5 2024年中国主要互联网应用用户规模排名")

add_para(
    "应用排名用横向柱状图做比较合适，标签不会被柱子挡住。"
    "即时通信排第一（10.7亿），微信QQ差不多全覆盖了。"
    "网络视频第二（10.5亿），抖音快手贡献很大。"
    "网络支付第三（9.8亿），基本上会上网的人就都会用移动支付了。"
    "搜索引擎8.9亿，网络购物8.7亿，都是国民级应用。"
)

add_para(
    "比较有意思的是在线教育和在线办公，"
    "2020年疫情的时候用的人暴增，"
    "后来虽然回落了但比疫情前还是多了不少。"
    "说明有些习惯一旦养成，确实回不去了。"
)

add_heading_styled("3.6 城乡差距", level=2)

add_chart(img("chart6_urban_rural.png"),
          "图6 中国城乡互联网普及率对比（2013-2024）")

add_para(
    "城乡差距这张图我做的分组柱状图，同一年城镇和农村放一起，差多少一眼就能看出来。"
    "城镇普及率从62.0%涨到了84.5%，农村从28.1%涨到了65.3%。"
    "农村虽然还比不过城镇，但增速快得多，十年涨了130%多。"
)

add_para(
    "差距从2013年的34个百分点缩小到了2024年的19个，"
    "数字鸿沟在变小，但将近20个点还是不小。"
    "这几年宽带下乡的政策确实有帮助，但要完全追上还得慢慢来。"
)

add_heading_styled("3.7 IP地址资源", level=2)

add_chart(img("chart7_ip.png"),
          "图7 中国IPv4/IPv6地址资源变化（2017-2024）")

add_para(
    "IP地址两张柱并排放，IPv4和IPv6此消彼长的关系很清楚。"
    "IPv4基本没涨，从3.39亿到3.62亿，"
    "因为IPv4地址早就分完了。"
    "IPv6就不一样了，从0.86亿涨到2.63亿，翻了快三倍。"
    "2017年国家发了文推IPv6部署，"
    "运营商和互联网公司都在跟进。"
    "看来IPv6全面取代IPv4只是时间问题。"
)

add_heading_styled("四、总结", level=1)

add_para(
    "总的说来，这十五年互联网变化确实大。"
    "网民涨到了11亿多，普及率快八成，但增长也差不多到头了。"
    "手机是绝对主流，做什么都得先考虑移动端。"
    "上网的人越来越多样，老人小孩都在上，"
    "城乡差距在缩小，但还有差距。"
    "IPv6也在快速铺开。"
)

add_para(
    "做这个报告最大的感受是，"
    "以前觉得CNNIC的报告就是些枯燥的数字，"
    "但真把这些数据画成图以后，"
    "很多趋势看一眼就明白了。"
    "数据可视化确实是个好东西。"
)

add_heading_styled("参考文献", level=1)

refs = [
    "[1] 中国互联网络信息中心. 第27次中国互联网络发展状况统计报告[R]. 北京, 2010.",
    "[2] 中国互联网络信息中心. 第37次中国互联网络发展状况统计报告[R]. 北京, 2015.",
    "[3] 中国互联网络信息中心. 第47次中国互联网络发展状况统计报告[R]. 北京, 2020.",
    "[4] 中国互联网络信息中心. 第51次中国互联网络发展状况统计报告[R]. 北京, 2022.",
    "[5] 中国互联网络信息中心. 第53次中国互联网络发展状况统计报告[R]. 北京, 2023.",
    "[6] 中国互联网络信息中心. 第55次中国互联网络发展状况统计报告[R]. 北京, 2024.",
    "[7] 中国互联网络信息中心. 第59次中国互联网络发展状况统计报告[R]. 北京, 2026.",
    "[8] 中共中央办公厅, 国务院办公厅. 推进互联网协议第六版（IPv6）规模部署行动计划[Z]. 2017.",
]
for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(ref)
    set_font(run, FONT_BODY, Pt(11))

if __name__ == "__main__":
    out_path = "/tmp/2308080119+王睿彬+数据源码.docx"
    doc.save(out_path)
    print(f"Report saved to: {out_path}")
    # NOTE: Windows mount lock prevents direct save to report/ dir.
    #       Manually copy from /tmp/ after closing any handle.
