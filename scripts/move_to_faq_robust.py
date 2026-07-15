from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

def extract_section(h2_text):
    target_h2 = None
    for h in soup.find_all('h2'):
        if h2_text in h.get_text():
            target_h2 = h
            break
            
    if not target_h2: return []
    
    start_block = target_h2
    while start_block.parent != content:
        start_block = start_block.parent
    start_idx = content.contents.index(start_block)
    
    end_idx = len(content.contents)
    for i in range(start_idx + 1, len(content.contents)):
        block = content.contents[i]
        if block.name and block.find('h2'):
            end_idx = i
            break
            
    blocks = content.contents[start_idx:end_idx]
    for b in blocks:
        b.extract()
    return blocks

blocks_layer = extract_section('ฉีดฟิลเลอร์สะโพกชั้นไหน')
blocks_duration = extract_section('ผลลัพธ์อยู่ได้นานแค่ไหน')
blocks_side_effects = extract_section('อาการข้างเคียงที่อาจเกิดขึ้นหลังฉีด')

all_qa_blocks = blocks_layer + blocks_duration + blocks_side_effects

for block in all_qa_blocks:
    if block.name:
        for h2 in block.find_all('h2'):
            h2.name = 'h3'
            h2['style'] = h2.get('style', '') + '; color: #476661;' # Match H3 styling if needed

# Create the new FAQ question
new_faq_html = """
<div class="row">
    <div class="col small-12 large-12">
        <h3 style="color: #476661;">ฉีดฟิลเลอร์สะโพกดีอย่างไร?</h3>
        <ul>
            <li>[Mockup: ช่วยปรับทรงสะโพกให้มีมิติและความอวบอิ่มมากขึ้น]</li>
            <li>[Mockup: ช่วยเพิ่มความมั่นใจในสัดส่วนและรูปร่าง]</li>
            <li>[Mockup: ไม่ต้องพักฟื้น ไม่มีแผลผ่าตัดขนาดใหญ่]</li>
            <li>[Mockup: เห็นผลลัพธ์ทันทีหลังทำ]</li>
        </ul>
    </div>
</div>
"""
new_faq_block = BeautifulSoup(new_faq_html, 'html.parser')
all_qa_blocks.append(new_faq_block)

summary_h2 = None
for h in soup.find_all('h2'):
    if 'บทสรุป' in h.get_text():
        summary_h2 = h
        break

if summary_h2:
    summary_block = summary_h2
    while summary_block.parent != content:
        summary_block = summary_block.parent
        
    qa_header = BeautifulSoup('<div class="row" style="margin-top: 40px; margin-bottom: 20px;"><div class="col small-12 large-12"><h2 style="color: #154a5c; text-align: center;">Q&amp;A คำถามที่พบบ่อย (FAQ)</h2></div></div>', 'html.parser')
    summary_block.insert_before(qa_header)
    
    for b in all_qa_blocks:
        summary_block.insert_before(b)
        
    # Handle the orphaned H3 "ฉีดสะโพกด้วยฟิลเลอร์ยี่ห้ออื่นได้ไหม"
    orphaned_h3 = None
    for h in soup.find_all('h3'):
        if 'ฉีดสะโพกด้วยฟิลเลอร์ยี่ห้ออื่นได้ไหม' in h.get_text():
            orphaned_h3 = h
            break
            
    if orphaned_h3:
        oblock = orphaned_h3
        while oblock.parent != content:
            oblock = oblock.parent
        oblock.extract()
        summary_block.insert_before(oblock)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Moved sections to Q&A successfully and added new question.')
else:
    print('Summary block not found.')
