from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

# Find the H2 for steps
steps_h2 = soup.find('h2', string=re.compile('ขั้นตอนการฉีดฟิลเลอร์สะโพก'))
if not steps_h2:
    print('H2 not found.')
    exit()

start_block = steps_h2
while start_block.parent != content:
    start_block = start_block.parent

start_idx = content.contents.index(start_block)

end_idx = len(content.contents)
for i in range(start_idx + 1, len(content.contents)):
    block = content.contents[i]
    if block.name and block.find('h2'):
        end_idx = i
        break

blocks = content.contents[start_idx:end_idx]

# Extract steps
steps = []
current_step = None

for b in blocks:
    if b == start_block: continue # Skip the H2 itself
    
    # Check if this block contains an H3 with 'ขั้นตอนที่'
    if b.name:
        for h3 in b.find_all('h3'):
            if 'ขั้นตอนที่' in h3.get_text():
                if current_step:
                    steps.append(current_step)
                current_step = {'title': h3.get_text(strip=True), 'img': None, 'text': []}
                # Remove the h3 from its old place so we don't duplicate it later
                h3.extract()
                
    if current_step:
        # Extract images
        if b.name:
            img = b.find('img')
            if img:
                current_step['img'] = img
                img.extract()
                
        # Extract text
        text = b.get_text(strip=True)
        if text and text != current_step['title']:
            current_step['text'].append(text)

if current_step:
    steps.append(current_step)

# Generate new HTML
if steps:
    new_html = '<div class="row" style="margin-bottom: 40px; margin-top: 20px;">'
    for step in steps:
        img_html = str(step['img']) if step['img'] else '<div style="background:#eee; height:200px; display:flex; align-items:center; justify-content:center; color:#999; border-radius:8px;">[No Image]</div>'
        text_html = '<br>'.join(step['text'])
        new_html += f'''
        <div class="col large-6 medium-6 small-12" style="margin-bottom: 30px;">
            <div style="background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); height: 100%;">
                <div style="text-align: center; margin-bottom: 15px;">
                    {img_html}
                </div>
                <h3 style="color: #476661; margin-bottom: 10px; font-size: 1.2em;">{step['title']}</h3>
                <p style="color: #666; font-size: 0.95em; line-height: 1.6;">{text_html}</p>
            </div>
        </div>
        '''
    new_html += '</div>'
    
    new_soup = BeautifulSoup(new_html, 'html.parser')
    
    # Remove old blocks (keep start_block which is the H2)
    for b in blocks[1:]:
        b.extract()
        
    start_block.insert_after(new_soup)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f'Successfully formatted {len(steps)} steps into 2 columns.')
else:
    print('No steps found.')
