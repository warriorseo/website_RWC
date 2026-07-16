import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

img = soup.find('img', src=re.compile('hip_filler_49.jpg$'))
if img:
    # Find the top level row for this image
    row = img.find_parent('div', class_='row')
    if row:
        new_html = """
        <div class="row" id="row-footer-4-columns" style="margin-top: 40px; margin-bottom: 40px; background-color: #ffffff; padding: 30px 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #f0f0f0;">
          <!-- Col 1: รู้จักหมอขนม -->
          <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px;">
            <div class="col-inner" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                  <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">รู้จักหมอขนม</h3>
                  <p style="font-size: 0.9em; color: #666; line-height: 1.5;">แพทย์ผู้เชี่ยวชาญด้านการปรับรูปหน้าและฉีดฟิลเลอร์สะโพก ประสบการณ์ยาวนาน</p>
              </div>
              <div style="margin-top: 15px;">
                  <a href="https://rwcclinic.com/dr-kanom-rwc/" style="display: inline-block; padding: 8px 20px; background-color: transparent; color: #154a5c; border-radius: 30px; text-decoration: none; font-size: 0.9em; border: 2px solid #154a5c; font-weight: bold; transition: all 0.3s ease;">อ่านประวัติแพทย์</a>
              </div>
            </div>
          </div>
          
          <!-- Col 2: Clinic Awards -->
          <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px; border-left: 1px solid #eee;">
            <div class="col-inner" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                  <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">Clinic Awards</h3>
                  <p style="font-size: 0.9em; color: #666; line-height: 1.5;">การันตีคุณภาพด้วยรางวัลระดับประเทศมากมาย มั่นใจในความปลอดภัย 100%</p>
              </div>
              <div style="margin-top: 15px;">
                  <a href="#" style="display: inline-block; padding: 8px 20px; background-color: transparent; color: #154a5c; border-radius: 30px; text-decoration: none; font-size: 0.9em; border: 2px solid #154a5c; font-weight: bold; transition: all 0.3s ease;">ดูรางวัลทั้งหมด</a>
              </div>
            </div>
          </div>

          <!-- Col 3: โปรโมชั่น -->
          <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px; border-left: 1px solid #eee;">
            <div class="col-inner" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                  <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">โปรโมชั่น</h3>
                  <p style="font-size: 0.9em; color: #666; line-height: 1.5;">อัปเดตโปรโมชั่นฉีดฟิลเลอร์สะโพก และบริการอื่นๆ ในราคาพิเศษสุดคุ้ม</p>
              </div>
              <div style="margin-top: 15px;">
                  <a href="#" style="display: inline-block; padding: 8px 20px; background-color: transparent; color: #154a5c; border-radius: 30px; text-decoration: none; font-size: 0.9em; border: 2px solid #154a5c; font-weight: bold; transition: all 0.3s ease;">ดูโปรโมชั่น</a>
              </div>
            </div>
          </div>

          <!-- Col 4: ติดต่อเรา -->
          <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px; border-left: 1px solid #eee;">
            <div class="col-inner" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                  <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">ติดต่อเรา</h3>
                  <p style="font-size: 0.9em; color: #666; line-height: 1.5;">ปรึกษาแพทย์ฟรี ไม่มีค่าใช้จ่าย<br>พร้อมดูแลคุณอย่างใกล้ชิด</p>
              </div>
              <div style="display: flex; justify-content: center; gap: 8px; margin-top: 15px;">
                <a href="https://lin.ee/dyBcDPC" target="_blank" style="display: inline-block; padding: 8px 12px; background-color: #00B900; color: white; border-radius: 30px; text-decoration: none; font-size: 0.85em; font-weight: bold; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,185,0,0.3);">LINE</a>
                <a href="https://m.me/102574639184550" target="_blank" style="display: inline-block; padding: 8px 12px; background-color: #0084FF; color: white; border-radius: 30px; text-decoration: none; font-size: 0.85em; font-weight: bold; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,132,255,0.3);">Messenger</a>
              </div>
            </div>
          </div>
        </div>
        """
        new_soup = BeautifulSoup(new_html, 'html.parser')
        row.replace_with(new_soup)
        
        # Add CSS for border-left handling on mobile and hover effects for buttons
        style_tag = soup.new_tag('style')
        style_tag.string = """
        @media (max-width: 849px) {
            #row-footer-4-columns .col {
                border-left: none !important;
                border-top: 1px solid #eee;
                margin-top: 15px;
                padding-top: 25px !important;
            }
            #row-footer-4-columns .col:first-child {
                border-top: none;
                margin-top: 0;
                padding-top: 10px !important;
            }
        }
        #row-footer-4-columns a {
            transition: all 0.3s ease;
        }
        #row-footer-4-columns a:hover {
            transform: translateY(-2px);
            opacity: 0.9;
        }
        """
        soup.head.append(style_tag)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Replaced image 49 with 4 columns layout.')
    else:
        print('Parent row not found for image 49.')
else:
    print('Image 49 not found.')
