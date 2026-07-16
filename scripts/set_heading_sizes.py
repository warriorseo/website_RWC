import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

style_tag = soup.find('style', id='custom-heading-sizes')
if style_tag:
    style_tag.decompose()

new_style = soup.new_tag('style', id='custom-heading-sizes')
new_style.string = """
    /* Enforce custom heading sizes requested by user */
    h2, .content-area h2 { font-size: 29px !important; }
    h3, .content-area h3 { font-size: 23px !important; }
"""

head = soup.find('head')
if head:
    head.append(new_style)
else:
    content = soup.find('div', class_='content-area')
    if content:
        content.insert(0, new_style)
    else:
        soup.insert(0, new_style)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print('Injected global heading font sizes (H2: 29px, H3: 23px).')
