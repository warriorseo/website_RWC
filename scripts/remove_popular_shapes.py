from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    
content = soup.find('div', class_='content-area')

h2 = None
for heading in soup.find_all('h2'):
    if 'ทรงสะโพกยอดนิยม' in heading.get_text():
        h2 = heading
        break

if h2:
    curr = h2
    while curr and curr.parent != content:
        curr = curr.parent
    
    idx = content.contents.index(curr)
    
    # We want to remove index 29, 31, 33 (which are relative to the found index)
    elements_to_remove = []
    for i in range(idx, idx + 6):
        if i < len(content.contents) and content.contents[i].name:
            # Check if we've reached the next H2
            if content.contents[i].find('h2'):
                if 'การปฏิบัติตัว' in content.contents[i].get_text():
                    break
            elements_to_remove.append(content.contents[i])
            
    for el in elements_to_remove:
        el.decompose()
    
    print("Removed Popular Shapes section.")
else:
    print("H2 not found.")

# Update TOC
toc = soup.find('a', href='#haunch23') # From previous script output, TOC link was #haunch23
if toc:
    li = toc.find_parent('li')
    if li:
        li.decompose()
        print("Removed TOC link.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
