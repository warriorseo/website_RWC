from bs4 import BeautifulSoup
import shutil

filepath_main = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
filepath_review = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/review_hip_filler_injection.html'

# 1. Create a copy for the review page
shutil.copy(filepath_main, filepath_review)

# 2. Process the Review Page (Keep ONLY the review blocks in content-area)
with open(filepath_review, 'r', encoding='utf-8') as f:
    soup_rev = BeautifulSoup(f.read(), 'html.parser')

content_rev = soup_rev.find('div', class_='content-area')

review_h2 = None
for h in soup_rev.find_all('h2'):
    if 'รีวิว' in h.get_text():
        review_h2 = h
        break

if review_h2:
    start_block = review_h2
    while start_block.parent != content_rev:
        start_block = start_block.parent
    start_idx = content_rev.contents.index(start_block)
    
    end_idx = len(content_rev.contents)
    for i in range(start_idx + 1, len(content_rev.contents)):
        block = content_rev.contents[i]
        if block.name and block.find('h2'):
            end_idx = i
            break
            
    # We want to keep ONLY from start_idx to end_idx.
    # We also probably want to keep the very top header/banner if possible, but for a simple cluster page, just clear everything else.
    blocks_to_keep = content_rev.contents[start_idx:end_idx]
    
    # Detach blocks_to_keep
    for b in blocks_to_keep:
        b.extract()
        
    content_rev.clear()
    
    # Optional: add a back button at the top
    back_btn = BeautifulSoup('<div class="row"><div class="col"><a href="hip_filler_injection.html" style="display:inline-block; margin: 20px 0; color: #154a5c; font-weight: bold;">&larr; กลับไปหน้าความรู้ฟิลเลอร์สะโพก</a></div></div>', 'html.parser')
    content_rev.append(back_btn)
    
    for b in blocks_to_keep:
        content_rev.append(b)
        
    with open(filepath_review, 'w', encoding='utf-8') as f:
        f.write(soup_rev.prettify())
    print("Created Review Page.")

# 3. Process the Main Page (Remove reviews and insert Mockup)
with open(filepath_main, 'r', encoding='utf-8') as f:
    soup_main = BeautifulSoup(f.read(), 'html.parser')

content_main = soup_main.find('div', class_='content-area')
review_h2_main = None
for h in soup_main.find_all('h2'):
    if 'รีวิว' in h.get_text():
        review_h2_main = h
        break

if review_h2_main:
    start_block = review_h2_main
    while start_block.parent != content_main:
        start_block = start_block.parent
    start_idx = content_main.contents.index(start_block)
    
    end_idx = len(content_main.contents)
    for i in range(start_idx + 1, len(content_main.contents)):
        block = content_main.contents[i]
        if block.name and block.find('h2'):
            end_idx = i
            break
            
    # Delete the original review blocks
    for i in range(start_idx, end_idx):
        content_main.contents[i].extract()
        
    # Create Mockup Block
    mockup_html = """
    <div class="row" style="margin-bottom: 40px;">
        <div class="col small-12 large-12 text-center" style="text-align: center;">
            <span class="scroll-to"><a name="haunch11"></a></span>
            <h2 style="color: #154a5c; text-align: center;">รีวิวการฉีดฟิลเลอร์สะโพก</h2>
            <p>ผลลัพธ์และความประทับใจจากคนไข้จริงกว่า 50+ เคส ที่เข้ารับบริการปั้นสะโพกสวยกับเรา</p>
            
            <div style="background-color: #f1f1f1; padding: 40px; border-radius: 8px; border: 2px dashed #ccc; margin-bottom: 20px;">
                <h3 style="color: #888;">[Mockup ภาพรีวิวตัวอย่าง 2-3 ภาพ]</h3>
            </div>
            
            <a href="review_hip_filler_injection.html" style="display: inline-block; background-color: #154a5c; color: white; padding: 15px 30px; font-size: 1.2em; border-radius: 5px; text-decoration: none;">👉 คลิกดูรีวิวและวิดีโอสัมภาษณ์คนไข้จริงทั้งหมด</a>
        </div>
    </div>
    """
    mockup_soup = BeautifulSoup(mockup_html, 'html.parser')
    
    # Insert Mockup where the original reviews were
    content_main.insert(start_idx, mockup_soup)

    with open(filepath_main, 'w', encoding='utf-8') as f:
        f.write(soup_main.prettify())
    print("Updated Main Page with Mockup.")
