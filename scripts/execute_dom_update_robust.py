from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

# 1. Remove the link
link = content.find('a', string=re.compile('ทำความรู้จักฟิลเลอร์ คืออะไร ได้ที่นี่'))
if link and link.parent.name == 'li':
    link.parent.decompose()
    print("Deleted the target link.")

# 2. Find TOC container
toc_text = content.find(string=re.compile('สารบัญฟิลเลอร์สะโพก'))
toc_container = toc_text
while toc_container and toc_container.parent != content:
    toc_container = toc_container.parent
print('Found TOC container.')

# 3. Find start container (first review text)
review_text = content.find(string=re.compile('ภาพรีวิวได้รับอนุญาตจากคนไข้เรียบร้อยแล้ว'))
start_container = review_text
while start_container and start_container.parent != content:
    start_container = start_container.parent
print('Found start container.')

# 4. Find dest container (Review H2)
dest_text = content.find(string=re.compile('รีวิวการฉีดฟิลเลอร์สะโพก'))
dest_container = dest_text
while dest_container and dest_container.parent != content:
    dest_container = dest_container.parent
print('Found dest container.')

if start_container and toc_container and dest_container:
    elements_to_move = []
    curr = start_container
    while curr and curr != toc_container:
        next_node = curr.next_sibling
        elements_to_move.append(curr)
        curr = next_node

    print(f"Found {len(elements_to_move)} elements to move.")

    for el in elements_to_move:
        el.extract()
        dest_container.insert_before(el)

    print("Moved elements successfully.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
else:
    print("Could not find all required containers.")
