import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

summary_h2 = soup.find(lambda tag: tag.name == 'h2' and 'สรุป' in tag.get_text())

if summary_h2:
    current = summary_h2.find_previous_sibling()
    count = 0
    while current:
        print(f"Deleting: {current.name} (class: {current.get('class') if current.name else ''})")
        temp = current.find_previous_sibling()
        current.decompose()
        current = temp
        count += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f'Deleted {count} elements right before Summary H2.')
else:
    print('Summary not found.')
