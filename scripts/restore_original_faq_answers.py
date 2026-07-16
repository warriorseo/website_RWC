import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

ans_duration = 'การฉีดฟิลเลอร์จะเข้าที่ใน 2 สัปดาห์ – 1 เดือน และผลลัพธ์อาจคงทนได้นานถึง 2 ปี ซึ่งผลลัพธ์จากการฉีดฟิลเลอร์สะโพกอาจแตกต่างกันไปในแต่ละบุคคล รวมถึงปัจจัยอื่น ๆ เช่น สุขภาพและการใช้ชีวิตประจำวันของผู้เข้ารับการรักษา<br><br><strong>| อ่านเพิ่มเติม:</strong> <a href=\"#\">ฟิลเลอร์สะโพก อยู่ได้นานแค่ไหน คุ้มค่าหรือไม่</a>'

ans_sidefx = 'สำหรับอาการข้างเคียงที่อาจเกิดขึ้นขณะฉีดหรือหลังฉีด คือ ภาวะฟกช้ำ หรือบริเวณสะโพกมีลักษณะบวมแดง นูน เป็นก้อน เขียวจากรอยเข็มในช่วง 1-3 วันแรก หรือความรู้สึกไม่สบายที่บริเวณที่ฉีด ทั้งนี้ อาการเหล่านี้จะค่อย ๆ ดีขึ้นตามลำดับค่ะ หากอาการไม่ดีขึ้น หรือมีอาการบวมที่ผิดปกติ แนะนำให้รีบเข้าพบแพทย์คลินิกที่ทำการรักษา<br><br><strong>| อ่านเพิ่มเติม:</strong> <a href=\"#\">หลังฉีดฟิลเลอร์บวมกี่วัน</a>'

accordion = soup.find('div', class_='accordion')
if accordion:
    items = accordion.find_all('div', class_='accordion-item')
    for item in items:
        # Avoid the '.simple-toggle' which is the + / -
        spans = item.find_all('span')
        title_text = ''
        for span in spans:
            if 'simple-toggle' not in span.get('class', []):
                title_text = span.get_text(strip=True)
                break
                
        inner = item.find('div', class_='accordion-inner')
        if inner and title_text:
            if 'ผลลัพธ์อยู่ได้นาน' in title_text:
                inner_soup = BeautifulSoup(f'<div class=\"accordion-inner\" style=\"display: none; padding: 15px; background: #f9f9f9; color: #555;\">{ans_duration}</div>', 'html.parser')
                inner.replace_with(inner_soup)
                print('Restored Duration answer.')
            elif 'อาการข้างเคียง' in title_text:
                inner_soup = BeautifulSoup(f'<div class=\"accordion-inner\" style=\"display: none; padding: 15px; background: #f9f9f9; color: #555;\">{ans_sidefx}</div>', 'html.parser')
                inner.replace_with(inner_soup)
                print('Restored SideFX answer.')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
else:
    print('Accordion not found.')
