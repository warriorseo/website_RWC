import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

faq_h2 = soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text())
summary_h2 = soup.find(lambda tag: tag.name == 'h2' and 'สรุป' in tag.get_text())

if faq_h2 and summary_h2:
    faq_top = faq_h2
    while faq_top.parent and 'content' not in (faq_top.parent.get('id') or '') and 'page-inner' not in faq_top.parent.get('class', []):
        if faq_top.parent.name == 'body':
            break
        faq_top = faq_top.parent

    summary_top = summary_h2
    while summary_top.parent and 'content' not in (summary_top.parent.get('id') or '') and 'page-inner' not in summary_top.parent.get('class', []):
        if summary_top.parent.name == 'body':
            break
        summary_top = summary_top.parent

    print('FAQ top element:', faq_top.name, faq_top.get('class'))
    print('Summary top element:', summary_top.name, summary_top.get('class'))
    
    if faq_top.parent == summary_top.parent:
        count = 0
        current = faq_top.find_next_sibling()
        while current and current != summary_top:
            temp = current.find_next_sibling()
            print(f'Deleting {current.name} (class: {current.get("class")})')
            current.decompose()
            current = temp
            count += 1
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f'Deleted {count} top-level elements between FAQ and Summary.')
    else:
        print('FAQ and Summary do not share the same top-level parent.')
else:
    print('Could not find FAQ or Summary H2.')
