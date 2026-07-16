import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Check if Noto Sans Thai is imported, if not, add it to head
head = soup.find('head')
if head:
    if not soup.find('link', href=re.compile('Noto\+Sans\+Thai')):
        font_link = soup.new_tag('link', rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&display=swap')
        head.append(font_link)
else:
    # insert at the top of content-area if no head
    content = soup.find('div', class_='content-area')
    if not soup.find('link', href=re.compile('Noto\+Sans\+Thai')):
        font_link = soup.new_tag('link', rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&display=swap')
        if content:
            content.insert(0, font_link)
        else:
            soup.insert(0, font_link)

# Find existing style block or create new one
style_tag = soup.find('style', id='custom-heading-sizes')
if style_tag:
    style_content = style_tag.string
    if 'Noto Sans Thai' not in style_content:
        style_tag.string = style_content + "\n    /* Apply Noto Sans Thai to all headings */\n    h1, h2, h3, h4, h5, h6, .content-area h1, .content-area h2, .content-area h3, .content-area h4, .content-area h5, .content-area h6 { font-family: 'Noto Sans Thai', sans-serif !important; }\n"
else:
    new_style = soup.new_tag('style', id='custom-heading-sizes')
    new_style.string = """
        /* Enforce custom heading sizes requested by user */
        h2, .content-area h2 { font-size: 29px !important; }
        h3, .content-area h3 { font-size: 23px !important; }
        /* Apply Noto Sans Thai to all headings */
        h1, h2, h3, h4, h5, h6, .content-area h1, .content-area h2, .content-area h3, .content-area h4, .content-area h5, .content-area h6 { font-family: 'Noto Sans Thai', sans-serif !important; }
    """
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
print('Applied Noto Sans Thai to all headings.')
