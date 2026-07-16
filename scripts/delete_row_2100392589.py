import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target_id = 'row-2100392589'
target_div = soup.find('div', id=target_id)
count = 0

if target_div:
    # also try to find the associated style tag
    prev_tag = target_div.find_previous_sibling('style')
    if prev_tag and target_id in prev_tag.get_text():
        prev_tag.decompose()
        count += 1
        
    next_tag = target_div.find_next_sibling('style')
    if next_tag and target_id in next_tag.get_text():
        next_tag.decompose()
        count += 1
        
    # Also find global style tags that might contain this ID
    style_tags = soup.find_all('style')
    for st in style_tags:
        if st.string and target_id in st.string:
            # We don't delete the whole style tag if it contains other things, but usually in Flatsome they are inline scoped
            if len(st.string.strip()) < 500: # heuristic for single scoped block
                st.decompose()
                count += 1
                
    target_div.decompose()
    count += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f'Deleted {count} elements related to {target_id}.')
else:
    print(f'{target_id} not found.')
