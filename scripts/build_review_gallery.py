import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# 1. Extract the 5 images and decompose their old containers
images = []
for i in range(37, 42):
    img = soup.find('img', src=re.compile(f'hip_filler_{i}.jpg'))
    if img:
        images.append(img['src'])
        # Find wrapper and decompose
        parent_col = img.find_parent('div', class_=lambda c: c and 'col ' in c)
        if parent_col:
            parent_row = parent_col.find_parent('div', class_='row')
            parent_col.decompose()
            if parent_row and not parent_row.find_all(recursive=False):
                parent_row.decompose()
        else:
            img.decompose()

if len(images) == 5:
    # 2. Build the 5-column gallery HTML
    gallery_html = '<div class="row row-small" id="review-gallery" style="margin-top: 30px; margin-bottom: 30px; display: flex; flex-wrap: wrap;">'
    for src in images:
        gallery_html += f"""
        <div class="col" style="flex: 1 1 20%; max-width: 20%; padding: 0 10px;">
            <div class="col-inner">
                <div class="img has-hover">
                    <div class="image-lightbox-wrapper">
                        <a href="{src}" class="image-lightbox">
                            <img src="{src}" alt="Review" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    # Mobile responsive CSS for the 5-column gallery will be added
    gallery_html += """
    <style>
        @media (max-width: 849px) {
            #review-gallery .col {
                flex: 1 1 50% !important;
                max-width: 50% !important;
                margin-bottom: 20px;
            }
        }
    </style>
    </div>
    """
    
    # 3. Find insertion point (before the review button)
    btn_text = 'ดูรีวิวหลังทำฟิลเลอร์สะโพกทั้งหมด'
    btn = soup.find(string=re.compile(btn_text))
    if btn:
        btn_parent_row = btn.find_parent('div', class_='row')
        if btn_parent_row:
            gallery_soup = BeautifulSoup(gallery_html, 'html.parser')
            btn_parent_row.insert_before(gallery_soup)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print('Built 5-column gallery and inserted before the review button.')
        else:
            print('Button row not found.')
    else:
        print('Review button not found.')
else:
    print('Could not find all 5 images.')
