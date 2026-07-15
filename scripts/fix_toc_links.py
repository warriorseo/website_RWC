from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

toc_heading = soup.find(string=re.compile('สารบัญเนื้อหา'))
if toc_heading:
    parent_row = toc_heading.find_parent('div', class_='row')
    if parent_row:
        ul = parent_row.find('ul')
        if ul:
            ul.clear()
            
            links = [
                ('ฟิลเลอร์สะโพก คืออะไร', '#haunch1'),
                ('เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร', '#haunch3'),
                ('ฉีดฟิลเลอร์สะโพกด้วยยี่ห้อ Variofill', '#haunch6'),
                ('เทคนิคและขั้นตอนการฉีดฟิลเลอร์สะโพก', '#haunch13'),
                ('ผลลัพธ์อยู่ได้นานแค่ไหน & อาการข้างเคียงที่อาจเกิดขึ้น', '#haunch5'),
                ('การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก', '#haunch4'),
                ('ฟิลเลอร์สะโพก ราคาเท่าไหร่', '#haunch14'),
                ('ฉีดฟิลเลอร์สะโพกกับหมอขนม (RWC Clinic) ดีอย่างไร', '#haunch12'),
                ('รีวิวการฉีดฟิลเลอร์สะโพก', '#haunch11'),
                ('Q&A คำถามที่พบบ่อย', '#haunch10')
            ]
            
            for title, href in links:
                li = soup.new_tag('li')
                li['style'] = "break-inside: avoid; margin-bottom: 10px;"
                a = soup.new_tag('a', href=href)
                span_title = soup.new_tag('span')
                span_title['style'] = "font-weight: 400;"
                span_title.string = title
                a.append(span_title)
                li.append(a)
                ul.append(li)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("TOC Links Hardcoded and Fixed.")
