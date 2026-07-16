import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

faq_row = soup.find('div', id='row-faq-content')
summary_h2 = soup.find(lambda tag: tag.name == 'h2' and 'สรุป' in tag.get_text())

if faq_row and summary_h2:
    summary_row = summary_h2.find_parent('div', class_='row')
    current = faq_row.find_next_sibling()
    
    print('Elements between FAQ and Summary:')
    count = 0
    while current and current != summary_row:
        if current.name:
            print(f"- {current.name} (id: {current.get('id')}, class: {current.get('class')})")
        temp = current.find_next_sibling()
        current.decompose()
        current = temp
        count += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f'Deleted {count} elements.')
else:
    print('FAQ or Summary not found.')
