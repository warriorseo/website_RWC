from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')
children = [c for c in content.contents if c.name]

# 1. Chunk into sections based on H2 presence
sections = []
current_section = []
current_h2_name = "TOP"

def get_h2_name(el):
    h2s = el.find_all('h2')
    if h2s:
        # Some blocks might have multiple H2s, return the first one
        return h2s[0].get_text().strip()
    return None

for child in children:
    h2_name = get_h2_name(child)
    if h2_name:
        if current_section:
            sections.append({'name': current_h2_name, 'elements': current_section})
        current_section = [child]
        current_h2_name = h2_name
    else:
        current_section.append(child)

if current_section:
    sections.append({'name': current_h2_name, 'elements': current_section})

# Helper to find and pop a section by partial name
def pop_section(partial_name):
    for i, s in enumerate(sections):
        if partial_name in s['name']:
            return sections.pop(i)
    return None

# Extract specific sections
sec_top = pop_section("TOP")
sec_toc = pop_section("สารบัญเนื้อหา")
sec_intro = pop_section("ฟิลเลอร์สะโพก คืออะไร")
sec_compare = pop_section("เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร")
sec_variofill1 = pop_section("ฟิลเลอร์สะโพก Variofill")
sec_variofill2 = pop_section("ฉีดฟิลเลอร์สะโพกด้วย Variofill")
sec_technique = pop_section("เทคนิคการฉีดฟิลเลอร์สะโพก")
sec_steps = pop_section("ขั้นตอนการฉีดฟิลเลอร์สะโพก")
sec_layer = pop_section("ฉีดฟิลเลอร์สะโพกชั้นไหน")
sec_results = pop_section("ผลลัพธ์อยู่ได้นานแค่ไหน")
sec_side_effects = pop_section("อาการข้างเคียงที่อาจเกิดขึ้นหลังฉีด")
sec_before_after = pop_section("การปฏิบัติตัวก่อน-หลัง")
sec_price = pop_section("ฟิลเลอร์สะโพก ราคาเท่าไหร่")
sec_doctor = pop_section("ฉีดฟิลเลอร์สะโพกกับหมอขนมดีอย่างไร")
sec_reviews = pop_section("รีวิวการฉีดฟิลเลอร์สะโพก")
sec_qa = pop_section("Q&A")
sec_summary = pop_section("บทสรุป")
sec_promo = pop_section("โปรโมชั่น")

# There is an awards section which is an H3, so it got bundled into the section before it.
# Wait, the mockup awards section was an H3. Let's see which section it ended up in.
# It should be in Q&A or Doctor.

# Any remaining sections?
print("Remaining sections not popped:")
for s in sections:
    print(" -", s['name'])

# Rebuild the list in the correct order
new_order = []
if sec_top: new_order.extend(sec_top['elements'])
if sec_toc: new_order.extend(sec_toc['elements'])
if sec_intro: new_order.extend(sec_intro['elements'])
if sec_compare: new_order.extend(sec_compare['elements'])

# Merge Variofill 1 and 2
if sec_variofill1: new_order.extend(sec_variofill1['elements'])
if sec_variofill2:
    # Rename the H2 in variofill 2 to just a strong text to avoid duplicate TOC
    h2 = sec_variofill2['elements'][0].find('h2')
    if h2 and "ศัลยกรรม" not in h2.get_text(): # Just in case
        h2.name = 'h3'
    new_order.extend(sec_variofill2['elements'])

if sec_technique: new_order.extend(sec_technique['elements'])
if sec_layer: new_order.extend(sec_layer['elements'])
if sec_steps: new_order.extend(sec_steps['elements'])
if sec_results: new_order.extend(sec_results['elements'])
if sec_side_effects: new_order.extend(sec_side_effects['elements'])
if sec_before_after: new_order.extend(sec_before_after['elements'])
if sec_price: new_order.extend(sec_price['elements'])
if sec_doctor: new_order.extend(sec_doctor['elements'])

# If any leftover sections are here (like awards if it was a separate H2), put them here
for s in sections:
    new_order.extend(s['elements'])

if sec_reviews: new_order.extend(sec_reviews['elements'])
if sec_qa: new_order.extend(sec_qa['elements'])
if sec_summary: new_order.extend(sec_summary['elements'])
if sec_promo: new_order.extend(sec_promo['elements'])

# Clear content-area and append in new order
content.clear()
for el in new_order:
    content.append(el)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("DOM Reordering Complete.")
