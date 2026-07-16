import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

faq_html = """
<div class="row" id="row-faq-header" style="margin-top: 40px;">
 <div class="col small-12 large-12 text-center">
  <h2 style="color: #154a5c; text-align: center; margin-bottom: 20px;">
   <strong>Q&amp;A คำถามที่พบบ่อย (FAQ)</strong>
  </h2>
 </div>
</div>
<div class="row" id="row-faq-content" style="margin-bottom: 40px;">
 <div class="col small-12 large-12">
  <div class="col-inner">
   <div class="accordion" rel="1">
    
    <div class="accordion-item">
     <a class="accordion-title plain" href="#" style="padding: 15px; border-bottom: 1px solid #eee; display: block; text-decoration: none; color: #333;">
      <span class="simple-toggle" style="margin-right: 10px; color: #154a5c; font-weight: bold;">+</span>
      <span>ผลลัพธ์อยู่ได้นานแค่ไหน</span>
     </a>
     <div class="accordion-inner" style="display: none; padding: 15px; background: #f9f9f9; color: #555;">
      ผลลัพธ์จากการฉีดฟิลเลอร์สะโพกสามารถอยู่ได้นาน 1-2 ปี ขึ้นอยู่กับการดูแลตัวเอง ยี่ห้อของฟิลเลอร์ที่เลือกใช้ และสภาพร่างกายของแต่ละบุคคล
     </div>
    </div>
    
    <div class="accordion-item">
     <a class="accordion-title plain" href="#" style="padding: 15px; border-bottom: 1px solid #eee; display: block; text-decoration: none; color: #333;">
      <span class="simple-toggle" style="margin-right: 10px; color: #154a5c; font-weight: bold;">+</span>
      <span>อาการข้างเคียงที่อาจเกิดขึ้นหลังฉีด</span>
     </a>
     <div class="accordion-inner" style="display: none; padding: 15px; background: #f9f9f9; color: #555;">
      อาจมีอาการบวมแดงหรือรอยช้ำเล็กน้อยบริเวณที่ฉีด ซึ่งเป็นอาการปกติและจะค่อยๆ หายไปเองภายใน 1-2 สัปดาห์ หากมีอาการปวดรุนแรงควรปรึกษาแพทย์ทันที
     </div>
    </div>
    
    <div class="accordion-item">
     <a class="accordion-title plain" href="#" style="padding: 15px; border-bottom: 1px solid #eee; display: block; text-decoration: none; color: #333;">
      <span class="simple-toggle" style="margin-right: 10px; color: #154a5c; font-weight: bold;">+</span>
      <span>ฉีดสะโพกด้วยฟิลเลอร์ยี่ห้ออื่นได้ไหม?</span>
     </a>
     <div class="accordion-inner" style="display: none; padding: 15px; background: #f9f9f9; color: #555;">
      ไม่ได้ค่ะ เนื่องจากสะโพกเป็นจุดที่ต้องใช้ตัวยาฟิลเลอร์ที่มีเทคโนโลยีและวัสดุที่ปลอดภัย มีความเข้มข้นสูง ถูกจัดอยู่ในกลุ่ม Cross-Linked มีลักษณะเป็นโมเลกุลที่มีอนุภาคเกาะกลุ่มกัน สามารถจัดรูปทรงขึ้นรูปง่าย ไม่กระจายตัว เป็นการออกแบบเพื่อฉีดสะโพกโดยเฉพาะ
     </div>
    </div>
    
   </div>
  </div>
 </div>
</div>
"""

old_faq_h2 = soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text())
if old_faq_h2:
    faq_row = old_faq_h2.find_parent('div', class_='row')
    
    # Let's see if accordion exists and decompose it
    accordion = soup.find('div', class_='accordion')
    if accordion:
        acc_row = accordion.find_parent('div', class_='row')
        if acc_row and acc_row != faq_row:
            acc_row.decompose()
        elif acc_row == faq_row:
            accordion.decompose()
            
    faq_soup = BeautifulSoup(faq_html, 'html.parser')
    faq_row.insert_before(faq_soup)
    faq_row.decompose()
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Restored full FAQ and removed first question.')
else:
    print('No FAQ H2 found.')
