import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

faq_h2 = soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text())
if faq_h2:
    faq_wrapper = faq_h2.find_parent('div', class_='col')
    if faq_wrapper:
        faq_row = faq_wrapper.find_parent('div', class_='row')
        if faq_row:
            # Find the last row in the FAQ section before the next H2
            last_faq_row = faq_row
            next_row = faq_row.find_next_sibling('div', class_='row')
            while next_row and not next_row.find('h2'):
                last_faq_row = next_row
                next_row = next_row.find_next_sibling('div', class_='row')
                
            new_faq_html = """
            <div class="row">
                <div class="col small-12 large-12">
                    <div class="col-inner">
                        <h3 style="color: #476661;"><strong><span style="color: #154a5c;">ฉีดสะโพกด้วยฟิลเลอร์ยี่ห้ออื่นได้ไหม?</span></strong></h3>
                        <p>ไม่ได้ค่ะ เนื่องจากสะโพกเป็นจุดที่ต้องใช้ตัวยาฟิลเลอร์ที่มีเทคโนโลยีและวัสดุที่ปลอดภัย มีความเข้มข้นสูง ถูกจัดอยู่ในกลุ่ม Cross-Linked มีลักษณะเป็นโมเลกุลที่มีอนุภาคเกาะกลุ่มกัน สามารถจัดรูปทรงขึ้นรูปง่าย ไม่กระจายตัว เป็นการออกแบบเพื่อฉีดสะโพกโดยเฉพาะ</p>
                    </div>
                </div>
            </div>
            """
            new_elements = BeautifulSoup(new_faq_html, 'html.parser')
            last_faq_row.insert_after(new_elements)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print('Added new FAQ successfully.')
        else:
            print('FAQ row not found.')
    else:
        print('FAQ col wrapper not found.')
else:
    print('FAQ H2 not found.')
