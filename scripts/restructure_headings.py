from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# 1. Update H2 Headings
h2_1 = soup.find('h2', string=re.compile('ฟิลเลอร์สะโพก คืออะไร'))
if h2_1:
    h2_1.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
    print("Updated H2: 'คืออะไร'")

h2_2 = soup.find('h2', string=re.compile('ฟิลเลอร์สะโพก ดีอย่างไร'))
if h2_2:
    # Remove the heading, but leave the content that follows it so it merges with the previous section
    # If the heading is wrapped in a row or col, we might need to be careful.
    # Let's check its parent.
    parent_row = h2_2.find_parent('div', class_='row')
    if parent_row and len(parent_row.find_all('h2')) == 1:
        # If the row just contains this heading and maybe some layout divs, we decompose the heading.
        # But wait, if the row ONLY contains the heading, we could decompose the row. 
        # But often the text is in a separate text block or the same row.
        # Let's just decompose the H2 and any empty wrapping divs if necessary.
        h2_2.decompose()
    else:
        h2_2.decompose()
    print("Removed H2: 'ดีอย่างไร' (Merged sections)")

h2_3 = soup.find('h2', string=re.compile('ฟิลเลอร์สะโพก เหมาะกับใครบ้าง'))
if h2_3:
    h2_3.string = "เช็กลิสต์: คุณเหมาะกับการปั้นสะโพกด้วยฟิลเลอร์หรือไม่?"
    print("Updated H2: 'เหมาะกับใครบ้าง'")


# 2. Update TOC Links
toc_1 = soup.find('a', href='#haunch1')
if toc_1:
    span = toc_1.find('span')
    if span:
        span.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
    else:
        toc_1.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
    print("Updated TOC: #haunch1")

toc_2 = soup.find('a', href='#haunch2')
if toc_2:
    li = toc_2.find_parent('li')
    if li:
        li.decompose()
    else:
        toc_2.decompose()
    print("Removed TOC: #haunch2")

toc_3 = soup.find('a', href='#haunch3')
if toc_3:
    span = toc_3.find('span')
    if span:
        span.string = "เช็กลิสต์: คุณเหมาะกับการปั้นสะโพกด้วยฟิลเลอร์หรือไม่?"
    else:
        toc_3.string = "เช็กลิสต์: คุณเหมาะกับการปั้นสะโพกด้วยฟิลเลอร์หรือไม่?"
    print("Updated TOC: #haunch3")


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("Saved HTML.")
