import re
from bs4 import BeautifulSoup

old_filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection_old.html'
new_filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'

try:
    with open(old_filepath, 'r', encoding='utf-16') as f:
        old_soup = BeautifulSoup(f.read(), 'html.parser')
except:
    with open(old_filepath, 'r', encoding='utf-8') as f:
        old_soup = BeautifulSoup(f.read(), 'html.parser')

with open(new_filepath, 'r', encoding='utf-8') as f:
    new_soup = BeautifulSoup(f.read(), 'html.parser')

# 1. Extract FAQ H2 row and Accordion row from old_soup
old_faq_h2 = old_soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text())
if old_faq_h2:
    faq_h2_row = old_faq_h2.find_parent('div', class_='row')
    accordion = old_soup.find('div', class_='accordion')
    accordion_row = accordion.find_parent('div', class_='row')
    
    # Check if they are already in the new soup to avoid duplicates
    if not new_soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text()):
        summary_h2 = new_soup.find(lambda tag: tag.name == 'h2' and 'สรุป' in tag.get_text())
        if summary_h2:
            summary_row = summary_h2.find_parent('div', class_='row')
            
            summary_row.insert_before(faq_h2_row)
            summary_row.insert_before(accordion_row)
            print('Restored FAQ section.')
            
            new_accordion = new_soup.find('div', class_='accordion')
            if new_accordion:
                items = new_accordion.find_all('div', class_='accordion-item')
                seen_titles = set()
                
                for item in items:
                    title_span = item.find('span')
                    title_text = title_span.get_text(strip=True) if title_span else ''
                    if not title_text or title_text == 'คำถาม' or title_text in seen_titles:
                        item.decompose()
                    else:
                        seen_titles.add(title_text)
                        
                items = new_accordion.find_all('div', class_='accordion-item')
                
                if items:
                    print(f"Removing first FAQ item: {items[0].find('span').get_text(strip=True)}")
                    items[0].decompose()
                    items = items[1:]
                    
                for item in items:
                    btn_toggle = item.find('button', class_='toggle')
                    if btn_toggle:
                        btn_toggle.decompose()
                    title_a = item.find('a', class_='accordion-title')
                    if title_a:
                        if not title_a.find('span', class_='simple-toggle'):
                            icon_span = new_soup.new_tag('span', class_='simple-toggle', style='margin-right: 10px; color: #154a5c; font-weight: bold;')
                            icon_span.string = '+'
                            title_a.insert(0, icon_span)

            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(new_soup.prettify())
            print('Cleaned up FAQ and removed the first question.')
        else:
            print('Summary H2 not found in new file.')
    else:
        print('FAQ is already in the new file.')
else:
    print('FAQ H2 not found in old file.')
