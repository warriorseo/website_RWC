import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

style_tag = soup.find('style', id='custom-heading-sizes')
if style_tag:
    style_content = style_tag.string
    if 'button, .button,' not in style_content:
        # replace the selector to include buttons
        old_selector = "h1, h2, h3, h4, h5, h6, .content-area h1, .content-area h2, .content-area h3, .content-area h4, .content-area h5, .content-area h6"
        new_selector = "h1, h2, h3, h4, h5, h6, .content-area h1, .content-area h2, .content-area h3, .content-area h4, .content-area h5, .content-area h6, button, .button, a.button"
        
        style_tag.string = style_content.replace(old_selector, new_selector)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Applied Noto Sans Thai to buttons.')
    else:
        print('Buttons already have Noto Sans Thai.')
else:
    print('Custom style tag not found.')
