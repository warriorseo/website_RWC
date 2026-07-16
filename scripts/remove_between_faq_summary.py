import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

faq_h2 = soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text())
summary_h2 = soup.find(lambda tag: tag.name == 'h2' and 'สรุป' in tag.get_text())

if faq_h2 and summary_h2:
    print('Found FAQ and Summary H2.')
    
    faq_row = faq_h2.find_parent('div', class_='row')
    summary_row = summary_h2.find_parent('div', class_='row')
    
    accordion = soup.find('div', class_='accordion')
    if accordion:
        start_row = accordion.find_parent('div', class_='row')
    else:
        start_row = faq_row
        
    current = start_row.find_next_sibling()
    count = 0
    while current and current != summary_row:
        temp = current.find_next_sibling()
        current.decompose()
        current = temp
        count += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f'Deleted {count} elements between FAQ and Summary.')
else:
    print('Could not find FAQ or Summary H2.')
