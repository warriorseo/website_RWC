from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

wrapper = soup.find('div', class_='custom-swiper-wrapper')

if wrapper:
    steps = []
    slides = wrapper.find_all('div', class_='swiper-slide')
    for slide in slides:
        img_container = slide.find('div', style=lambda s: s and 'display: flex' in s)
        img = img_container.find('img') if img_container else None
        if img: img.extract()
        
        title = slide.find('h3').get_text(strip=True) if slide.find('h3') else 'ขั้นตอน'
        p = slide.find('p')
        text = str(p.decode_contents()) if p else ''
        
        steps.append({'img': img, 'title': title, 'text': text})

    if steps:
        grid_html = """
        <div class="steps-grid-wrapper" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; background-color: #f0f7f6; padding: 60px 0; margin-bottom: 40px; margin-top: 20px;">
            <div style="max-width: 1600px; margin: 0 auto; padding: 0 20px;">
                <div class="steps-flex-container" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">
        """
        
        for step in steps:
            img_html = str(step['img']).replace('style="', 'style="max-width: 100%; height: auto; border-radius: 8px; ') if step['img'] else '<div style="background:#ddd; width:100%; height:150px; display:flex; align-items:center; justify-content:center; color:#999; border-radius:8px;">[No Image]</div>'
            grid_html += f"""
                    <div class="step-card" style="flex: 1 1 12%; min-width: 150px; background-color: #fff; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); display: flex; flex-direction: column; overflow: hidden;">
                        <div style="width: 100%; padding: 15px; background-color: #fcfcfc; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #eee;">
                            {img_html}
                        </div>
                        <div style="width: 100%; padding: 20px 15px; text-align: center;">
                            <h3 style="color: #476661; font-size: 1.1em; margin-bottom: 10px; font-weight: bold;">{step['title']}</h3>
                            <p style="color: #666; font-size: 0.85em; line-height: 1.5;">{step['text']}</p>
                        </div>
                    </div>
            """
            
        grid_html += """
                </div>
            </div>
            <style>
                @media (max-width: 1200px) {
                    .step-card { flex: 1 1 20% !important; }
                }
                @media (max-width: 768px) {
                    .step-card { flex: 1 1 45% !important; min-width: 45% !important; }
                }
                @media (max-width: 480px) {
                    .step-card { flex: 1 1 100% !important; }
                }
            </style>
        </div>
        """
        
        new_soup = BeautifulSoup(grid_html, 'html.parser')
        wrapper.replace_with(new_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Successfully replaced Swiper with a static 7-column Flexbox grid.')
    else:
        print('Could not extract steps data from existing wrapper.')
else:
    print('Wrapper not found.')
