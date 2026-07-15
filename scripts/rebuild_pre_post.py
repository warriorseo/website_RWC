from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

target_h2 = None
for h in soup.find_all('h2'):
    if 'การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก' in h.get_text():
        target_h2 = h
        break

if target_h2:
    start_block = target_h2
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
    
    # Extract before lists
    before_h3 = None
    after_h3 = None
    for b in blocks:
        if b.name:
            for h3 in b.find_all('h3'):
                if 'ก่อนฉีด' in h3.get_text():
                    before_h3 = h3
                elif 'หลังฉีด' in h3.get_text():
                    after_h3 = h3

    before_lis = []
    if before_h3:
        parent = before_h3.find_parent('div', class_='col') or before_h3.parent
        ul = parent.find('ul') if hasattr(parent, 'find') else None
        if ul:
            before_lis = [li.get_text(strip=True) for li in ul.find_all('li')]

    after_lis = []
    if after_h3:
        parent = after_h3.find_parent('div', class_='col') or after_h3.parent
        ul = parent.find('ul') if hasattr(parent, 'find') else None
        if ul:
            after_lis = [li.get_text(strip=True) for li in ul.find_all('li')]

    # Create new layout
    new_html = f"""
    <div class="row" style="margin-bottom: 40px;">
        <div class="col small-12 large-12">
            <h2 style="color: #154a5c; text-align: center; margin-bottom: 30px;">การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก</h2>
        </div>
        
        <!-- Before Column -->
        <div class="col medium-6 small-12">
            <h3 style="color: #476661; text-align: center;">ข้อควรปฏิบัติก่อนฉีด</h3>
            <div style="text-align: center; margin-bottom: 20px;">
                <a href="http://localhost:8081/images/hip_filler_19.jpg" class="image-lightbox" title="ข้อควรปฏิบัติก่อนฉีด">
                    <img src="http://localhost:8081/images/hip_filler_19.jpg" alt="ก่อนฉีดฟิลเลอร์สะโพก" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); cursor: pointer; max-height: 400px; width: auto;" />
                </a>
                <p style="font-size: 0.8em; color: #888; margin-top: 5px;">(คลิกที่ภาพเพื่อขยาย)</p>
            </div>
            <ul style="color: #49687e; font-size: 1em; line-height: 1.6;">
                {"".join([f'<li style="margin-bottom: 10px;">{li}</li>' for li in before_lis])}
            </ul>
        </div>
        
        <!-- After Column -->
        <div class="col medium-6 small-12">
            <h3 style="color: #476661; text-align: center;">ข้อควรปฏิบัติหลังฉีด</h3>
            <div style="text-align: center; margin-bottom: 20px;">
                <a href="http://localhost:8081/images/hip_filler_20.jpg" class="image-lightbox" title="ข้อควรปฏิบัติหลังฉีด">
                    <img src="http://localhost:8081/images/hip_filler_20.jpg" alt="หลังฉีดฟิลเลอร์สะโพก" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); cursor: pointer; max-height: 400px; width: auto;" />
                </a>
                <p style="font-size: 0.8em; color: #888; margin-top: 5px;">(คลิกที่ภาพเพื่อขยาย)</p>
            </div>
            <ul style="color: #49687e; font-size: 1em; line-height: 1.6;">
                {"".join([f'<li style="margin-bottom: 10px;">{li}</li>' for li in after_lis])}
            </ul>
        </div>
    </div>
    """
    
    new_soup = BeautifulSoup(new_html, 'html.parser')
    
    for b in blocks:
        b.extract()
        
    content.insert(start_idx, new_soup)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Rebuilt pre and post care section.')
else:
    print('H2 not found.')
