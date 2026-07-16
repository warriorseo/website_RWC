import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Fix "4."
for h3 in soup.find_all('h3'):
    text = h3.get_text()
    if '4.' in text and 'ฉีดสะโพกด้วยฟิลเลอร์' in text:
        for string_node in h3.find_all(string=re.compile(r'4\.\s*')):
            string_node.replace_with(string_node.replace('4. ', '').replace('4.', ''))

faq_h2 = soup.find(lambda tag: tag.name == 'h2' and 'FAQ' in tag.get_text())
if faq_h2:
    faq_wrapper = faq_h2.find_parent('div', class_='col')
    if faq_wrapper:
        faq_row = faq_wrapper.find_parent('div', class_='row')
        if faq_row:
            faq_rows = []
            next_row = faq_row.find_next_sibling('div', class_='row')
            while next_row and not next_row.find('h2'):
                faq_rows.append(next_row)
                next_row = next_row.find_next_sibling('div', class_='row')
                
            if faq_rows:
                accordion_html = '<div class="accordion" rel="1">'
                for row in faq_rows:
                    h3 = row.find('h3')
                    question_text = h3.get_text(strip=True) if h3 else 'คำถาม'
                    
                    answer_content = ''
                    col_inner = row.find('div', class_='col-inner')
                    if col_inner:
                        for child in col_inner.children:
                            if getattr(child, 'name', None) not in ['h3', 'span'] and getattr(child, 'name', None) is not None:
                                answer_content += str(child)
                                
                    accordion_html += f"""
                    <div class="accordion-item">
                        <a href="#" class="accordion-title plain">
                            <button class="toggle"><i class="icon-angle-down"></i></button>
                            <span>{question_text}</span>
                        </a>
                        <div class="accordion-inner" style="display: none;">
                            {answer_content}
                        </div>
                    </div>
                    """
                accordion_html += '</div>'
                
                new_soup = BeautifulSoup(accordion_html, 'html.parser')
                
                container_html = """
                <div class="row" style="margin-bottom: 40px;">
                    <div class="col small-12 large-12">
                        <div class="col-inner">
                        </div>
                    </div>
                </div>
                """
                container_soup = BeautifulSoup(container_html, 'html.parser')
                container_soup.find('div', class_='col-inner').append(new_soup)
                
                faq_row.insert_after(container_soup)
                
                for row in faq_rows:
                    row.decompose()
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print('Converted FAQ to Accordion successfully.')
            else:
                print('No FAQ questions found.')
        else:
            print('FAQ row not found.')
    else:
        print('FAQ col not found.')
else:
    print('FAQ H2 not found.')
