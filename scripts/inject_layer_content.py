import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target_text = 'สำหรับการฉีดฟิลเลอร์เสริมสะโพก'
found = soup.find(string=re.compile(target_text))
if found:
    p_tag = found.find_parent('p')
    if p_tag:
        new_html = """
        <h2 style="color: #154a5c; margin-top: 40px; margin-bottom: 20px;">ฉีดฟิลเลอร์สะโพกชั้นไหน?</h2>
        <p>โปรแกรมฉีดฟิลเลอร์สะโพก หรือการฉีดสารเติมเต็มเพื่อเพิ่มขนาดในบริเวณสะโพกสามารถทำได้ในชั้นไขมัน โดยการฉีดในชั้นนี้เป็นการฉีดที่มีความปลอดภัยสูง เพราะอยู่ภายใต้ชั้นกล้ามเนื้อ ไม่มีเส้นเลือดที่อันตรายและไม่มีเส้นประสาท จึงสามารถมั่นใจได้ว่า ฉีดฟิลเลอร์สะโพกแล้วจะไม่มีโอกาสฟิลเลอร์อุดตันในเส้นเลือดแน่นอน</p>
        """
        new_elements = BeautifulSoup(new_html, 'html.parser')
        p_tag.insert_after(new_elements)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Injected new content successfully.')
