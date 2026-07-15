from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

target_h2 = None
for h in soup.find_all('h2'):
    if 'เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร' in h.get_text():
        target_h2 = h
        break

if target_h2:
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
            
    blocks_to_delete = content.contents[start_idx + 1:end_idx]
    for b in blocks_to_delete:
        b.extract()
        
    placeholder_html = """
    <div class="row" style="margin-bottom: 30px; margin-top: 20px;">
        <div class="col small-12 large-12">
            <div style="background-color: #f5f5f5; border: 2px dashed #ccc; padding: 40px; text-align: center; border-radius: 8px;">
                <h3 style="color: #888; margin-bottom: 20px;">[Mockup: เนื้อหาเปรียบเทียบฟิลเลอร์ vs ศัลยกรรม]</h3>
                <p style="color: #555; font-size: 1.2em;">ตรงนี้จะเป็นพื้นที่สำหรับเขียนเนื้อหาใหม่ทั้งหมด เพื่อเปรียบเทียบข้อดี-ข้อเสียอย่างละเอียด</p>
                <div style="background-color: #e0e0e0; height: 300px; max-width: 600px; margin: 30px auto 0 auto; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 1px solid #ccc;">
                    <span style="color: #666; font-size: 1.1em; font-weight: bold;">[Placeholder Image: ตารางเปรียบเทียบ หรือ รูปภาพประกอบ]</span>
                </div>
            </div>
        </div>
    </div>
    """
    
    placeholder_soup = BeautifulSoup(placeholder_html, 'html.parser')
    start_block.insert_after(placeholder_soup)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Replaced content with placeholders.')
else:
    print('H2 not found.')
