from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

# 1. Remove the link "ทำความรู้จักฟิลเลอร์ คืออะไร ได้ที่นี่"
link = content.find('a', string=re.compile('ทำความรู้จักฟิลเลอร์ คืออะไร ได้ที่นี่'))
if link and link.parent.name == 'li':
    link.parent.decompose()
    print("Deleted the target link.")

# 2. Find the bounds for moving
# Find TOC
toc_h2 = content.find(lambda t: t.name in ['h2', 'span', 'div', 'h3'] and 'สารบัญ' in t.get_text())
toc_container = toc_h2.find_parent('div', recursive=False)
if toc_container.parent == content:
    pass
else:
    # Go up until child of content
    curr = toc_h2
    while curr.parent != content:
        curr = curr.parent
    toc_container = curr

# Find first review p
review_p = content.find('p', string=re.compile('ภาพรีวิวได้รับอนุญาตจากคนไข้เรียบร้อยแล้ว'))
start_container = review_p.find_parent('div', class_='row')

# Collect all siblings from start_container up to toc_container
elements_to_move = []
curr = start_container
while curr and curr != toc_container:
    next_node = curr.next_sibling
    elements_to_move.append(curr)
    curr = next_node

print(f"Found {len(elements_to_move)} elements to move.")

# Find destination: review section
dest_h2 = content.find('h2', string=re.compile('รีวิวการฉีดฟิลเลอร์สะโพก'))
dest_container = dest_h2.find_parent('div', class_='row')
if not dest_container:
    curr = dest_h2
    while curr.parent != content:
        curr = curr.parent
    dest_container = curr

# Insert elements before dest_container
for el in elements_to_move:
    # detach
    el.extract()
    # insert
    dest_container.insert_before(el)

print("Moved elements successfully.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
