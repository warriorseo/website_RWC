from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

def get_top_level(element):
    curr = element
    while curr and curr.parent != content:
        curr = curr.parent
    return curr

# 1. Find elements
intro_text = content.find(string=re.compile('ภาพรีวิวได้รับอนุญาตจากคนไข้เรียบร้อยแล้ว'))
vid1_text = content.find(string=re.compile('ส่องรีวิวฉีดฟิลเลอร์สะโพก'))
vid2_text = content.find(string=re.compile('รีวิวฉีดฟิลเลอร์สะโพก คุณมีน'))
h2_review = content.find(string=re.compile('รีวิวการฉีดฟิลเลอร์สะโพก'))

# 2. Get their top-level containers
intro_cont = get_top_level(intro_text) if intro_text else None
vid1_cont = get_top_level(vid1_text) if vid1_text else None
vid2_cont = get_top_level(vid2_text) if vid2_text else None
h2_cont = get_top_level(h2_review) if h2_review else None

# 3. Reorder them
if h2_cont:
    # Extract scattered elements
    elements_to_move = []
    if intro_cont and intro_cont != h2_cont:
        intro_cont.extract()
        elements_to_move.append(intro_cont)
    if vid1_cont and vid1_cont != h2_cont:
        vid1_cont.extract()
        elements_to_move.append(vid1_cont)
    if vid2_cont and vid2_cont != h2_cont:
        vid2_cont.extract()
        elements_to_move.append(vid2_cont)
        
    # Insert them after H2, in order: intro, vid1, vid2
    # But wait, what if h2_cont contains the gallery?
    # Yes, h2_cont might be just the row with the heading. Let's insert after it.
    target = h2_cont
    for el in elements_to_move:
        target.insert_after(el)
        target = el
        
    print("Consolidated reviews successfully.")
else:
    print("H2 Review not found!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
