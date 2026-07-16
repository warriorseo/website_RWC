import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

footer = soup.find('div', id='row-footer-4-columns')
if footer:
    style = footer.get('style', '')
    if 'display: flex' not in style:
        style += ' display: flex; flex-wrap: wrap; justify-content: center;'
    footer['style'] = style
    
    # Let's ensure the cols are taking exactly 25% on desktop
    style_tag = soup.new_tag('style')
    style_tag.string = """
    #row-footer-4-columns {
        display: flex;
        flex-wrap: wrap;
        width: 100%;
        max-width: 100% !important;
    }
    #row-footer-4-columns > .col {
        flex: 0 0 25%;
        max-width: 25%;
        padding: 10px;
    }
    @media (max-width: 849px) {
        #row-footer-4-columns > .col {
            flex: 0 0 50%;
            max-width: 50%;
        }
    }
    @media (max-width: 549px) {
        #row-footer-4-columns > .col {
            flex: 0 0 100%;
            max-width: 100%;
        }
    }
    """
    soup.head.append(style_tag)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Enforced flexbox and exact column widths.')
else:
    print('Footer not found.')
