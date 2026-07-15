from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

# 1. Move promo banners down
promo_elements = []
for i in range(2):
    img = content.find('img', src=f'images/hip_filler_{i}.jpg')
    if img:
        # Find the direct child of content-area that contains this image
        curr = img
        while curr and curr.parent != content:
            curr = curr.parent
        if curr and curr not in promo_elements:
            promo_elements.append(curr)

price_heading = content.find(string=lambda t: t and 'ฟิลเลอร์สะโพก ราคาเท่าไหร่' in t)
if price_heading:
    price_curr = price_heading
    while price_curr and price_curr.parent != content:
        price_curr = price_curr.parent
    
    # Insert promo elements after the price heading
    target = price_curr
    for el in promo_elements:
        el.extract()
        target.insert_after(el)
        target = el # Next one goes after this one
    print(f"Moved {len(promo_elements)} promo banner blocks down to price section.")

# 2. Move Hero video to the very top
vid = content.find(string=lambda t: t and 'เรื่องต้องรู้ก่อนฉีดฟิลเลอร์สะโพก' in t)
if vid:
    vid_curr = vid
    while vid_curr and vid_curr.parent != content:
        vid_curr = vid_curr.parent
    
    if vid_curr:
        vid_curr.extract()
        content.insert(0, vid_curr)
        print("Moved Hero video to the very top.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
