from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

steps_h2 = None
for h in soup.find_all('h2'):
    if 'ขั้นตอนการฉีดฟิลเลอร์สะโพก' in h.get_text():
        steps_h2 = h
        break

if steps_h2:
    start_block = steps_h2
    while start_block.parent != content:
        start_block = start_block.parent
        
    start_idx = content.contents.index(start_block)
    
    steps_row = None
    for i in range(start_idx + 1, len(content.contents)):
        block = content.contents[i]
        if block.name == 'div' and 'row' in block.get('class', []):
            steps_row = block
            break
            
    if steps_row:
        steps = []
        for col in steps_row.find_all('div', class_=lambda c: c and 'col ' in c):
            img = col.find('img')
            if img: img.extract()
            h3 = col.find('h3')
            title = h3.get_text(strip=True) if h3 else 'ขั้นตอน'
            p = col.find('p')
            text = str(p.decode_contents()) if p else ''
            steps.append({'img': img, 'title': title, 'text': text})
            
        if steps:
            carousel_html = """
            <div class="steps-carousel-wrapper" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; background-color: #f0f7f6; padding: 60px 0; margin-bottom: 40px; margin-top: 20px;">
                <div class="row">
                    <div class="col small-12 large-12">
                        <div class="slider-wrapper relative">
                            <div class="slider slider-nav-circle slider-nav-large slider-style-normal" data-flickity-options='{"cellAlign": "center", "imagesLoaded": true, "wrapAround": true, "autoPlay": 6000, "pageDots": true, "prevNextButtons": true}'>
            """
            
            for step in steps:
                img_html = str(step['img']).replace('style="', 'style="max-width: 100%; border-radius: 8px; ') if step['img'] else '<div style="background:#ddd; height:100%; min-height: 300px; display:flex; align-items:center; justify-content:center; color:#999; border-radius:12px;">[No Image]</div>'
                carousel_html += f"""
                                <div class="col small-12 large-12" style="padding: 0 15px;">
                                    <div class="row align-middle" style="background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin: 20px 0;">
                                        <div class="col medium-6 small-12" style="padding: 0;">
                                            <div style="height: 100%; display: flex; align-items: center; justify-content: center; background-color: #fcfcfc;">
                                                {img_html}
                                            </div>
                                        </div>
                                        <div class="col medium-6 small-12" style="padding: 50px 40px;">
                                            <h3 style="color: #476661; font-size: 2em; margin-bottom: 20px; font-weight: bold; text-align: left;">{step['title']}</h3>
                                            <p style="color: #666; font-size: 1.1em; line-height: 1.8; text-align: left;">{step['text']}</p>
                                        </div>
                                    </div>
                                </div>
                """
                
            carousel_html += """
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            
            new_soup = BeautifulSoup(carousel_html, 'html.parser')
            steps_row.replace_with(new_soup)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print('Successfully transformed steps into a full-width carousel banner.')
        else:
            print('Could not extract steps data.')
    else:
        print('Steps row not found.')
else:
    print('H2 not found.')
