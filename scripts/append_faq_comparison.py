import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

new_faq_html = """
<div class="accordion-item">
 <a class="accordion-title plain" href="#" style="padding: 15px; border-bottom: 1px solid #eee; display: block; text-decoration: none; color: #333;">
  <span class="simple-toggle" style="margin-right: 10px; color: #154a5c; font-weight: bold;">+</span>
  <span>ฟิลเลอร์สะโพก ศัลยกรรมสะโพก และฉีดไขมันสะโพก แตกต่างกันอย่างไร?</span>
 </a>
 <div class="accordion-inner" style="display: none; padding: 15px; background: #f9f9f9; color: #555;">
  <p style="margin-bottom: 10px;">ทั้ง 3 วิธีมีความแตกต่างกันตามจุดประสงค์และผลลัพธ์ที่ได้ค่ะ:</p>
  <ul style="margin-left: 20px; margin-bottom: 0;">
   <li style="margin-bottom: 10px;"><strong>การฉีดฟิลเลอร์สะโพก:</strong> เป็นการใช้สารเติมเต็ม ปลอดภัยสูง ไม่ต้องพักฟื้น เห็นผลทันทีและสามารถจัดทรงได้ตามต้องการ</li>
   <li style="margin-bottom: 10px;"><strong>การศัลยกรรมสะโพก:</strong> คล้ายการเสริมหน้าอกโดยใช้ซิลิโคนสำหรับก้นโดยเฉพาะ อยู่ได้ถาวร แต่ต้องใช้เวลาพักฟื้นนานและมีความเสี่ยงจากการผ่าตัด</li>
   <li><strong>การฉีดไขมันสะโพก:</strong> นำไขมันของตนเองจากส่วนอื่นมาฉีดเสริมเพื่อเพิ่มขนาดและยกกระชับก้นให้สวยงาม 
       <strong>| อ่านเพิ่มเติม:</strong> <a href="https://rwcclinic.com/fat-grafting-face/" style="color: #154a5c; text-decoration: underline;" target="_blank">การฉีดไขมัน (Fat Grafting)</a>
   </li>
  </ul>
 </div>
</div>
"""

accordion = soup.find('div', class_='accordion')
if accordion:
    new_item = BeautifulSoup(new_faq_html, 'html.parser')
    accordion.append(new_item)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Appended new FAQ item.')
else:
    print('Accordion not found.')
