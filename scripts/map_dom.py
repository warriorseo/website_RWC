from bs4 import BeautifulSoup

with open('d:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

for i, child in enumerate(content.children):
    if child.name:
        text = child.get_text(strip=True)[:50]
        classes = child.get('class', [])
        print(f'Child {i}: <{child.name} class="{classes}"> - {text}')
