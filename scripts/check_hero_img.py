from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

img = soup.find('img', src=lambda s: s and 'hip_filler_0.jpg' in s)
if img:
    print('Parent tree of img 0:')
    parent = img.parent
    while parent and parent.name != 'body':
        if parent.name:
            classes = parent.get('class', [])
            print(f'-> {parent.name} .{".".join(classes)}')
        parent = parent.parent
        
    content_area = soup.find('div', class_='content-area')
    if content_area:
        print('Is img inside content-area?', img in content_area.descendants)
        # Find position inside content-area
        for i, child in enumerate(content_area.children):
            if child.name and img in child.descendants:
                print(f'Img is inside content_area.children[{i}], which is a {child.name} with classes {child.get("class")}')
                break
else:
    print('Image not found.')
