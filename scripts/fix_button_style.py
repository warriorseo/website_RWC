from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find the awards link
awards_link = soup.find('a', href='https://rwcclinic.com/our-awards/')
if awards_link:
    # 1. Update text to remove emoji
    awards_link.string = "ดูความสำเร็จและรางวัลทั้งหมดของเรา คลิกที่นี่"
    
    # 2. Update styles (Change red #d83131 to clinic theme #154a5c)
    # the original style: "display: inline-block; background-color: #d83131; color: #fff; padding: 10px 25px; border-radius: 5px; font-weight: bold; text-decoration: none;"
    new_style = "display: inline-block; background-color: #154a5c; color: #fff; padding: 10px 25px; border-radius: 5px; font-weight: normal; text-decoration: none; border: 1px solid #154a5c;"
    awards_link['style'] = new_style
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Updated button style and removed emoji.")
else:
    print("Awards link not found.")
