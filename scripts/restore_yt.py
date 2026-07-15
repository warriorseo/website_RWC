from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

hero_img = soup.find('img', src=lambda x: x and 'hip_filler_0.jpg' in x)
if hero_img:
    hero_container = hero_img.find_parent('div', class_=lambda c: c and 'img ' in c)
    if not hero_container:
        hero_container = hero_img
        
    yt_html = """
    <div class="row" style="margin-top: 40px; margin-bottom: 20px;">
        <div class="col small-12 large-12">
            <h2 style="color: #154a5c; text-align: center; margin-bottom: 20px;">คลิปเดียวจบ : ฟิลเลอร์สะโพกเหมาะกับใคร? ใครอยากฉีดห้ามพลาดคลิปนี้</h2>
            <div class="video video-fit mb" style="padding-top:56.25%; position: relative; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" title="YouTube video player" src="https://www.youtube.com/embed/8ULmmnz8gXA?autoplay=0&controls=1&rel=0&showinfo=0" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
            </div>
        </div>
    </div>
    """
    new_soup = BeautifulSoup(yt_html, 'html.parser')
    
    hero_container.insert_after(new_soup)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Successfully restored YouTube video at the top.')
else:
    print('Hero image not found.')
