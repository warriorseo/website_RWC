from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

def robust_find_h2(text_to_find):
    for h2 in soup.find_all('h2'):
        if text_to_find in h2.get_text():
            return h2
    return None

# 1. Restore "คืออะไร"
# Currently the first H2 is "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
# Let's change it back to "ฟิลเลอร์สะโพก คืออะไร"
h2_first = robust_find_h2('เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร')
if h2_first:
    h2_first.string = "ฟิลเลอร์สะโพก คืออะไร"
    print("Restored H2: 'ฟิลเลอร์สะโพก คืออะไร'")

# 2. Change "เช็กลิสต์" to "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
# Because the user said they don't want "เหมาะกับใคร" (which became เช็กลิสต์) and "ดีอย่างไร",
# they just want the "ดีกว่าศัลยกรรมอย่างไร" heading.
h2_checklist = robust_find_h2('เช็กลิสต์')
if h2_checklist:
    h2_checklist.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
    print("Updated H2: 'เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร'")
    
    # Replace the mockup checklist with a placeholder for the new topic
    p = h2_checklist.find_next_sibling('p')
    if p and 'ทีมลูกค้า' in p.get_text():
        p.string = "[ทีมลูกค้า: กรุณาใส่เนื้อหาเปรียบเทียบข้อดีของการฉีดฟิลเลอร์เทียบกับการผ่าตัดเสริมซิลิโคนตรงนี้]"
        # Remove the ul checklist
        ul = p.find_next_sibling('ul')
        if ul and 'color: #666' in ul.get('style', ''):
            ul.decompose()

# 3. Update TOC
toc = soup.find(string=re.compile('สารบัญเนื้อหา'))
if toc:
    ul = toc.find_next('ul')
    if ul:
        # Recreate the TOC items for the first two
        for li in ul.find_all('li'):
            a = li.find('a')
            if a and a.get('href') == '#haunch1':
                span = a.find('span')
                if span:
                    span.string = "ฟิลเลอร์สะโพก คืออะไร"
                else:
                    a.string = "ฟิลเลอร์สะโพก คืออะไร"
            
            if a and a.get('href') == '#haunch3':
                span = a.find('span')
                if span:
                    span.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
                else:
                    a.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("Saved HTML.")
