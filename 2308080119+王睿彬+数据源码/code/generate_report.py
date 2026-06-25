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
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

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
    row.height = Cm(0.65)

    cell0 = row.cells[0]
    cell0.width = Cm(3.2)
    remove_cell_margins(cell0)
    cell0.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.BOTTOM
    cell0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    cell0.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
    cell0.paragraphs[0].paragraph_format.space_before = Pt(0)
    cell0.paragraphs[0].paragraph_format.space_after = Pt(0)
    cell0.paragraphs[0].paragraph_format.line_spacing = 1.0
    run0 = cell0.paragraphs[0].add_run(f"{label}：")
    run0.font.size = Pt(15)
    run0.font.name = FONT_BODY
    run0.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

    cell1 = row.cells[1]
    cell1.width = Cm(8)
    remove_cell_margins(cell1)
    cell1.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.BOTTOM
    cell1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell1.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
    cell1.paragraphs[0].paragraph_format.space_before = Pt(0)
    cell1.paragraphs[0].paragraph_format.space_after = Pt(0)
    cell1.paragraphs[0].paragraph_format.line_spacing = 1.0
    run1 = cell1.paragraphs[0].add_run(value)
    run1.font.size = Pt(15)
    run1.font.name = FONT_BODY
    run1.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

    tc = cell1._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), '000000')
    tcBorders.append(bottom)
    if tcBorders not in tcPr:
        tcPr.append(tcBorders)

def set_border_none(cell, side):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
    border = tcBorders.find(qn(f'w:{side}'))
    if border is None:
        border = OxmlElement(f'w:{side}')
    border.set(qn('w:val'), 'none')
    border.set(qn('w:sz'), '0')
    border.set(qn('w:space'), '0')
    border.set(qn('w:color'), 'auto')
    tcBorders.append(border)
    if tcBorders not in tcPr:
        tcPr.append(tcBorders)

for row in table.rows:
    for cell in row.cells:
        for side in ['top', 'left', 'right']:
            set_border_none(cell, side)

doc.add_page_break()

# ====== 正文 ======

add_heading_styled("一、引言", level=1)

add_para(
    "从2010年到现在，中国互联网的变化真的太大了。"
    "2010年那会儿3G刚普及，智能手机还是个贵东西，上网主要是用电脑。"
    "现在呢，一部手机什么都搞定了——聊天、买东西、看视频、点外卖、交水电费。"
    "这背后其实反映了很多层面的变化：网络基础设施的升级、终端设备的普及、"
    "用户群体的扩张和分化、应用生态的丰富，以及城乡之间数字鸿沟的演变。"
    "这些变化不是孤立的，它们互相影响、共同推动了中国互联网的快速发展。"
)

add_para(
    "中国互联网络信息中心（CNNIC）从1997年开始，每半年发布一次"
    "《中国互联网络发展状况统计报告》，至今已经发布了五十多次。"
    "这份报告被国内外广泛引用，可以说是研究中国互联网最权威的数据来源之一。"
    "报告中记录了网民规模、普及率、接入设备、用户结构、"
    "应用使用情况、基础设施建设等多个维度的指标，时间跨度长、指标体系稳定，"
    "非常适合用来做趋势分析。"
)

add_para(
    "本报告选取了2010年到2025年这个时间窗口，主要原因有两个："
    "一是这十五年恰好是中国互联网从起步到成熟的关键阶段，"
    "3G商用、4G爆发、5G部署都发生在这个时期；"
    "二是CNNIC在这段时间内的调查方法和指标体系相对稳定，"
    "数据具有较好的连续性和可比性。"
    "我从中提取了七个核心维度：网民规模与普及率、手机网民、"
    "年龄结构、学历结构、互联网应用排名、城乡普及率对比、IP地址资源。"
    "每个维度都选择了最能反映其特征的图表类型，"
    "后面会逐一说明选图的理由。"
)

add_para(
    "可视化工具方面，我用了PyECharts和Matplotlib两个库。"
    "PyECharts基于ECharts，可以生成交互式网页图表，"
    "用浏览器打开以后能够悬停看数据、缩放、筛选，交互性比较强，"
    "适合用来探索数据。Matplotlib是Python最经典的绘图库，"
    "生成的静态图表格式规范、适合打印和排版。"
    "两种工具结合使用，网页端做交互探索，"
    "打印端看静态图表，各有各的用途。"
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
    "网民从2010年的4.57亿涨到了2025年的11.25亿，普及率从34.3%到了79.8%。"
    "柱状图拆网民规模、折线搭普及率，两个量纲不一样但放到一起能对照着看。"
    "前十年涨得特别快，每年基本多四五千万人，那会儿正好3G变4G、"
    "智能手机也越来越便宜。2020年后增速慢了，一年就多两三千万——"
    "该上的都上了，剩下的增量本来就不多。"
)

add_heading_styled("3.2 手机网民", level=2)

add_chart(img("chart2_mobile.png"),
          "图2 中国手机网民规模及占比变化（2010-2025）")

add_para(
    "2010年手机上网才66.2%，三分之一的人还用电脑。"
    "2025年到了99.9%，基本全民手机上网了。"
    "双轴图一边标规模一边标占比，量纲不统一也能各看各的趋势。"
)

add_para(
    "2015年是个转折点，那一年手机占比第一次破90%。"
    "之后电脑用户越来越少，谁还专门开电脑上网啊。"
    "移动支付、短视频、外卖能在中国做得这么好，跟这个趋势有很大关系。"
)

add_heading_styled("3.3 年龄结构", level=2)

add_chart(img("chart3_age.png"),
          "图3 中国网民年龄结构演变（2013-2024）")

add_para(
    "2013年50岁以上网民加起来才7.6%，2024年到了22.8%，"
    "60岁以上从2.5%涨到7.6%。我爸妈以前根本不碰手机，"
    "现在天天刷短视频、发红包，数据跟身边的情况对得上。"
    "堆叠柱状图的好处是每年的构成和年份间的变化都能看出来。"
)

add_para(
    "年轻人占比反而降了不少，20到29岁从31.2%降到18.7%。"
    "但我觉得不是年轻人不上网了，是老年人进来太多被稀释了。"
    "30到39岁一直稳定在20%到24%，40到49岁从12.5%涨到21.5%。"
)

add_heading_styled("3.4 学历结构", level=2)

add_chart(img("chart4_education.png"),
          "图4 2024年中国网民学历结构分布")

add_para(
    "2024年学历分布比较平均。初中学历最多32.8%，"
    "高中/中专26.2%，大专/本科27.6%，小学及以下8.8%，硕士以上4.6%。"
    "环形图看分类占比挺直观的。"
    "高学历比例在慢慢涨，大专及以上从2013年的20.9%到了32.2%。"
    "不过初中及以下的群体还是很大，做产品的人得考虑到这一点。"
)

add_heading_styled("3.5 互联网应用", level=2)

add_chart(img("chart5_apps.png"),
          "图5 2024年中国主要互联网应用用户规模排名")

add_para(
    "即时通信10.7亿排第一，网络视频10.5亿第二，"
    "网络支付9.8亿第三，搜索引擎8.9亿，网络购物8.7亿。"
    "一开始我用的纵向柱状图，应用名称太长挤成一团，"
    "换成横向的就好了，标签完整显示，排序也清楚。"
)

add_para(
    "在线教育4.2亿、在线办公5.3亿，"
    "疫情的时候用的人暴增，后来回落了一些但还是比疫情前多。"
    "有些习惯养成之后就回不去了。"
)

add_heading_styled("3.6 城乡差距", level=2)

add_chart(img("chart6_urban_rural.png"),
          "图6 中国城乡互联网普及率对比（2013-2024）")

add_para(
    "城镇普及率62.0%涨到84.5%，农村从28.1%涨到65.3%。"
    "农村虽然绝对值还落后，但增速更快，十年涨了130%多。"
    "分组柱状图每年两根柱子挨着，差距变化一目了然。"
    "从34个百分点缩到19个，数字鸿沟在变小，但将近20个点还是不小。"
)

add_heading_styled("3.7 IP地址资源", level=2)

add_chart(img("chart7_ip.png"),
          "图7 中国IPv4/IPv6地址资源变化（2017-2024）")

add_para(
    "IPv4从3.39亿到3.62亿，基本没动——全球IPv4早就分完了。"
    "IPv6从0.86亿涨到2.63亿，翻了快三倍。"
    "两根柱并排放，反差很清楚。"
    "2017年国家推IPv6部署之后增速明显加快，"
    "全面取代IPv4应该只是时间问题。"
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
    "做这个报告之前我翻过几次CNNIC的报告，"
    "密密麻麻的数字看完也记不住什么。"
    "但把数据画成图以后，增长最快的是哪几年、"
    "哪个年龄段变化最大、城乡差距到底多大，"
    "一眼就能抓住。"
    "数据可视化确实是个好工具。"
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
