import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target_id = 'image_1822682657'
target_div = soup.find('div', id=target_id)
count = 0

if target_div:
    parent_div = target_div.find_parent('div', style=re.compile('margin-top: 40px;'))
    if parent_div:
        parent_div.decompose()
        count += 1
    else:
        # Just delete the target div itself if parent is not exactly matching
        target_div.decompose()
        count += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f'Deleted {count} elements related to {target_id}.')
else:
    print(f'{target_id} not found.')
