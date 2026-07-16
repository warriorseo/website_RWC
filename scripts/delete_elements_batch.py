import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

count = 0

# 1. Delete image_1822682657
target_id = 'image_1822682657'
target_div = soup.find('div', id=target_id)
if target_div:
    parent_div = target_div.find_parent('div', style=re.compile('margin-top: 40px;'))
    if parent_div:
        parent_div.decompose()
        count += 1
    else:
        target_div.decompose()
        count += 1

# 2. Delete Mockup Data for Awards
mockup_span = soup.find(lambda tag: tag.name == 'span' and '[ภาพ Mockup Data: รวมรางวัล RWC Clinic]' in tag.get_text())
if mockup_span:
    row_div = mockup_span.find_parent('div', class_='row')
    if row_div:
        row_div.decompose()
        count += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print(f'Deleted {count} elements.')
