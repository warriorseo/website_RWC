from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Update TOC
toc = soup.find(string=re.compile('สารบัญเนื้อหา'))
if toc:
    ul = toc.find_next('ul')
    if ul:
        ul.clear()
        
        # Helper to add li
        def add_li(title, target_h2_text):
            # Find the H2 in the document to get its parent's ID or its anchor
            h2 = soup.find('h2', string=re.compile(target_h2_text))
            anchor_name = ''
            if h2:
                # Look for an anchor tag above it
                span = h2.find_previous_sibling('span', class_='scroll-to')
                if span:
                    a = span.find('a')
                    if a and a.has_attr('name'):
                        anchor_name = '#' + a['name']
            
            if anchor_name:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=anchor_name)
                span_title = soup.new_tag('span')
                span_title['style'] = "font-weight: 400;"
                span_title.string = title
                a.append(span_title)
                li.append(a)
                ul.append(li)

        add_li('ฟิลเลอร์สะโพก คืออะไร', 'ฟิลเลอร์สะโพก คืออะไร')
        add_li('เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร', 'เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร')
        add_li('ฉีดฟิลเลอร์สะโพกด้วยยี่ห้อ Variofill', 'ฟิลเลอร์สะโพก Variofill') # The first variofill section
        add_li('เทคนิคและขั้นตอนการฉีดฟิลเลอร์สะโพก', 'เทคนิคการฉีดฟิลเลอร์สะโพก')
        add_li('ผลลัพธ์อยู่ได้นานแค่ไหน & อาการข้างเคียงที่อาจเกิดขึ้น', 'ผลลัพธ์อยู่ได้นานแค่ไหน')
        add_li('การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก', 'การปฏิบัติตัวก่อน-หลัง')
        add_li('ฟิลเลอร์สะโพก ราคาเท่าไหร่', 'ราคาเท่าไหร่')
        add_li('ฉีดฟิลเลอร์สะโพกกับหมอขนม (RWC Clinic) ดีอย่างไร', 'หมอขนม')
        add_li('รีวิวการฉีดฟิลเลอร์สะโพก', 'รีวิวการฉีดฟิลเลอร์สะโพก')
        
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("TOC Updated.")
