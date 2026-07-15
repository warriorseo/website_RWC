from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

# Extract all valid children (skip empty text nodes for indexing)
children = [c for c in content.contents if c.name]

# Helper to find which child index contains a specific H2
def find_block_index(h2_text):
    for i, child in enumerate(children):
        for h2 in child.find_all('h2'):
            if h2_text in h2.get_text():
                return i
    return -1

# Let's see the actual indices in the filtered list
print("TOC:", find_block_index('สารบัญเนื้อหา'))
print("intro:", find_block_index('ฟิลเลอร์สะโพก คืออะไร'))
print("compare:", find_block_index('เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร'))
print("before_after:", find_block_index('การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก'))
print("side_effects:", find_block_index('อาการข้างเคียงที่อาจเกิดขึ้นหลังฉีด'))
print("variofill_1:", find_block_index('ฟิลเลอร์สะโพก Variofill'))
print("results:", find_block_index('ผลลัพธ์อยู่ได้นานแค่ไหน'))
print("price:", find_block_index('ฟิลเลอร์สะโพก ราคาเท่าไหร่'))
print("technique:", find_block_index('เทคนิคการฉีดฟิลเลอร์สะโพก'))
print("steps:", find_block_index('ขั้นตอนการฉีดฟิลเลอร์สะโพก'))
print("layer:", find_block_index('ฉีดฟิลเลอร์สะโพกชั้นไหน?'))
print("variofill_2_vs:", find_block_index('ฉีดฟิลเลอร์สะโพกด้วย Variofill'))
print("doctor:", find_block_index('ฉีดฟิลเลอร์สะโพกกับหมอขนมดีอย่างไร'))
print("qa:", find_block_index('Q&A'))
print("reviews:", find_block_index('รีวิวการฉีดฟิลเลอร์สะโพก'))
print("summary:", find_block_index('บทสรุป'))
print("promo:", find_block_index('โปรโมชั่นฟิลเลอร์สะโพก'))
