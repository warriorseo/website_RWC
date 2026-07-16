import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

style_tag = soup.find('style', id='custom-heading-sizes')
if style_tag:
    style_content = style_tag.string
    if 'button, .button { background-color: transparent' not in style_content:
        style_tag.string = style_content + """
        /* Force buttons to be outline */
        button, .button, a.button { 
            background-color: transparent !important; 
            border: 2px solid #154a5c !important; 
            color: #154a5c !important; 
        }
        button:hover, .button:hover, a.button:hover {
            background-color: #154a5c !important;
            color: #ffffff !important;
        }
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Applied global outline CSS for buttons.')
    else:
        print('Global outline CSS already applied.')
else:
    print('Style tag not found.')
