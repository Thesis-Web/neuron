from pathlib import Path
import re
import sys
import json
import hashlib
from zipfile import ZipFile
sys.path.insert(0, '/home/exnulla/Downloads/.neuron-document-tools/lib')
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
source = ROOT / 'Neuron-Thesis.md'
md = source.read_text()
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.top_margin, sec.bottom_margin = Inches(.85), Inches(.8)
sec.left_margin, sec.right_margin = Inches(.95), Inches(.95)
sec.header_distance, sec.footer_distance = Inches(.35), Inches(.35)
sec.different_first_page_header_footer = True
styles = doc.styles
for name in ['Normal', 'Body Text']:
    style = styles[name]
    style.font.name = 'Cambria'
    style.font.size = Pt(11)
    style.font.color.rgb = RGBColor.from_string('20252B')
    style.paragraph_format.line_spacing = 1.16
    style.paragraph_format.space_after = Pt(8)
    style.paragraph_format.widow_control = True
for name, size in [('Title', 30), ('Subtitle', 16), ('Heading 1', 21), ('Heading 2', 14)]:
    style = styles[name]
    style.font.name = 'Calibri'
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor.from_string('243C53')
    style.paragraph_format.keep_with_next = True
    style.paragraph_format.space_before = Pt(14)
    style.paragraph_format.space_after = Pt(10)
styles['Heading 1'].paragraph_format.page_break_before = False
styles['Heading 1'].paragraph_format.space_before = Pt(23)
styles['Heading 2'].paragraph_format.space_before = Pt(12)

header = sec.header.paragraphs[0]
header.text = 'NEURON  /  EXPERIENCE AS EXECUTABLE STRUCTURE'
header.style = styles['Caption']
header.runs[0].font.size = Pt(8)
header.runs[0].font.color.rgb = RGBColor.from_string('657487')
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('Neuron thesis  ·  ')
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)
for run in footer.runs:
    run.font.name = 'Calibri'
    run.font.size = Pt(9)

bookmark_id = 0
def bookmark(p, name):
    global bookmark_id
    bookmark_id += 1
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(bookmark_id))
    start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), str(bookmark_id))
    p._p.insert(0, start)
    p._p.append(end)

def link(p, text, anchor):
    h = OxmlElement('w:hyperlink')
    h.set(qn('w:anchor'), anchor)
    r = OxmlElement('w:r')
    props = OxmlElement('w:rPr')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '365D7D')
    props.append(color)
    r.append(props)
    t = OxmlElement('w:t')
    t.text = text
    r.append(t)
    h.append(r)
    p._p.append(h)

def prose(p, text):
    pos = 0
    for match in re.finditer(r'\[(S\d{2}(?:, S\d{2})*)\]', text):
        p.add_run(text[pos:match.start()])
        p.add_run('[')
        for i, ref in enumerate(match.group(1).split(', ')):
            if i:
                p.add_run(', ')
            link(p, ref, ref)
        p.add_run(']')
        pos = match.end()
    p.add_run(text[pos:])

paragraphs = md.split('\n\n')
in_contents = False
for block in paragraphs:
    block = block.strip()
    if not block:
        continue
    if block.startswith('# '):
        p = doc.add_paragraph(block[2:], 'Title')
        p.paragraph_format.space_before = Pt(90)
        continue
    if block.startswith('## A thesis'):
        doc.add_paragraph(block[3:], 'Subtitle')
        continue
    if block.startswith('## '):
        title = block[3:]
        in_contents = title == 'Contents'
        p = doc.add_heading(title, level=1)
        if title in ['Abstract', 'Reading this manuscript', 'Contents'] or title.startswith(('1. ', 'Appendix ')):
            p.paragraph_format.page_break_before = True
        m = re.match(r'(\d+)\.', title)
        if m:
            bookmark(p, 'chapter_' + m.group(1))
        elif title.startswith('Appendix A'):
            bookmark(p, 'appendix_A')
        elif title.startswith('Appendix B'):
            bookmark(p, 'appendix_B')
        continue
    if block.startswith('### '):
        title = block[4:]
        p = doc.add_heading(title, level=2)
        m = re.match(r'(S\d{2})\.', title)
        if m:
            bookmark(p, m.group(1))
        continue
    if in_contents:
        for line in block.splitlines():
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.0
            m = re.match(r'(\d+)\.', line)
            anchor = ('chapter_' + m.group(1)) if m else ('appendix_A' if line.startswith('Appendix A') else 'appendix_B')
            link(p, line, anchor)
        continue
    p = doc.add_paragraph()
    prose(p, block.replace('\n', ' '))

doc.core_properties.title = 'Neuron: Experience as Executable Structure'
doc.core_properties.subject = 'A thesis of the Neuron system within Cortex'
doc.core_properties.author = 'Codex — synthesis of the project owner’s conceptual work'
doc.core_properties.keywords = 'Neuron, Cortex, mathematical graph, executable memory, learning'
doc.core_properties.comments = 'Prepared 2026-10-15 from cited Cortex records. Conceptual authorship belongs to the project owner.'
out = ROOT / 'Neuron-Thesis.docx'
doc.save(out)

# Validate the complete paragraph text, including text inside hyperlinks.
from lxml import etree
with ZipFile(out) as z:
    root = etree.fromstring(z.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
actual = [''.join(p.xpath('.//w:t/text()', namespaces=ns)) for p in root.xpath('//w:body/w:p', namespaces=ns)]
expected = []
for block in paragraphs:
    block = block.strip()
    if not block:
        continue
    if block.startswith('#'):
        expected.append(re.sub(r'^#{1,3} ', '', block))
    elif re.match(r'^1\. The problem', block):
        expected.extend(block.splitlines())
    else:
        expected.append(block.replace('\n', ' '))
assert actual == expected, 'DOCX text differs from Markdown'
anchors = set(root.xpath('//w:bookmarkStart/@w:name', namespaces=ns))
links = root.xpath('//w:hyperlink/@w:anchor', namespaces=ns)
assert all(a in anchors for a in links), 'Broken internal link'
refs = set(re.findall(r'S\d{2}', md))
assert refs == {'S%02d' % i for i in range(1, 26)}
chapters = re.findall(r'^## (\d+)\.', md, re.M)
assert chapters == [str(i) for i in range(1, 25)]
assert not re.search(r'^(?:\+|TODO|TBD|PLACEHOLDER)', md, re.M)

manifest = {
    'title': doc.core_properties.title,
    'date': '2026-10-15',
    'word_count_markdown': len(md.split()),
    'chapters': len(chapters),
    'source_entries': 25,
    'retrieved_source_files': len(list((ROOT / 'sources').glob('*.txt'))),
    'internal_links': len(links),
    'validation': 'DOCX paragraph text matches Markdown; chapter sequence and link targets verified',
    'files': {}
}
for path in [source, out, *sorted((ROOT / 'sources').glob('*.txt'))]:
    manifest['files'][str(path.relative_to(ROOT))] = {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
(ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({k:v for k,v in manifest.items() if k != 'files'}, indent=2))

