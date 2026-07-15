from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

review_h2 = None
for h in soup.find_all('h2'):
    if 'รีวิวการฉีดฟิลเลอร์สะโพก' in h.get_text():
        review_h2 = h
        break

if review_h2:
    parent_row = review_h2
    while parent_row.parent != content:
        parent_row = parent_row.parent
        
    mockup_html = """
    <div class="row" style="margin-bottom: 50px;">
        <div class="col small-12 large-12 text-center" style="text-align: center;">
            <span class="scroll-to"><a name="haunch11"></a></span>
            <h2 style="color: #154a5c; text-align: center; margin-bottom: 10px;">รีวิวการฉีดฟิลเลอร์สะโพก</h2>
            <p style="margin-bottom: 30px;">ผลลัพธ์และความประทับใจจากคนไข้จริงกว่า 50+ เคส ที่เข้ารับบริการปั้นสะโพกสวยกับ RWC Clinic</p>
        </div>
        
        <!-- Video Row -->
        <div class="col medium-6 small-12">
            <div class="col-inner">
                <div style="background-color: #000; height: 300px; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative;">
                    <span style="color: #fff; font-size: 16px;">[Mockup: Video Review 1]</span>
                    <div style="position: absolute; width: 60px; height: 40px; background-color: red; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><span style="color:white; font-size: 20px;">▶</span></div>
                </div>
            </div>
        </div>
        <div class="col medium-6 small-12">
            <div class="col-inner">
                <div style="background-color: #000; height: 300px; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative;">
                    <span style="color: #fff; font-size: 16px;">[Mockup: Video Review 2]</span>
                    <div style="position: absolute; width: 60px; height: 40px; background-color: red; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><span style="color:white; font-size: 20px;">▶</span></div>
                </div>
            </div>
        </div>
        
        <!-- Image Gallery Row -->
        <div class="col small-12 large-12" style="margin-top: 20px;">
            <div class="row">
                <div class="col medium-3 small-6">
                    <div class="col-inner has-lightbox">
                        <a href="#" class="lightbox-link">
                            <div style="background-color: #f1f1f1; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc;">
                                <span style="color: #888; font-size: 14px; text-align: center;">[Mockup]<br>Image 1<br>(Click to Pop-up)</span>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col medium-3 small-6">
                    <div class="col-inner has-lightbox">
                        <a href="#" class="lightbox-link">
                            <div style="background-color: #f1f1f1; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc;">
                                <span style="color: #888; font-size: 14px; text-align: center;">[Mockup]<br>Image 2<br>(Click to Pop-up)</span>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col medium-3 small-6">
                    <div class="col-inner has-lightbox">
                        <a href="#" class="lightbox-link">
                            <div style="background-color: #f1f1f1; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc;">
                                <span style="color: #888; font-size: 14px; text-align: center;">[Mockup]<br>Image 3<br>(Click to Pop-up)</span>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col medium-3 small-6">
                    <div class="col-inner has-lightbox">
                        <a href="#" class="lightbox-link">
                            <div style="background-color: #f1f1f1; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc;">
                                <span style="color: #888; font-size: 14px; text-align: center;">[Mockup]<br>Image 4<br>(Click to Pop-up)</span>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Action Button -->
        <div class="col small-12 large-12 text-center" style="text-align: center; margin-top: 30px;">
            <a href="review_hip_filler_injection.html" class="button primary is-large box-shadow-2 box-shadow-4-hover" style="border-radius: 5px;">
                <span>ดูรีวิวและวิดีโอเคสจริงทั้งหมด</span>
            </a>
        </div>
    </div>
    """
    
    mockup_soup = BeautifulSoup(mockup_html, 'html.parser')
    parent_row.replace_with(mockup_soup)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Injected Professional Mockup.")
else:
    print("Could not find review H2.")
