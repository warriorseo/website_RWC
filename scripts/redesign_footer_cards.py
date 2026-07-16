import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

footer = soup.find('div', id='row-footer-4-columns')
if footer:
    new_html = """
    <div class="row" id="row-footer-4-columns" style="margin-top: 20px; margin-bottom: 40px;">
      <!-- Card 1: รู้จักหมอขนม -->
      <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px;">
        <div class="col-inner card-layout">
          <div>
              <div class="icon-wrapper">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              </div>
              <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">รู้จักหมอขนม</h3>
              <p style="font-size: 0.9em; color: #666; line-height: 1.5;">แพทย์ผู้เชี่ยวชาญด้านการปรับรูปหน้าและฉีดฟิลเลอร์สะโพก ประสบการณ์ยาวนาน</p>
          </div>
          <div style="margin-top: 15px;">
              <a href="https://rwcclinic.com/dr-kanom-rwc/" class="btn-card">อ่านประวัติแพทย์</a>
          </div>
        </div>
      </div>
      
      <!-- Card 2: โปรโมชั่น (Swapped) -->
      <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px;">
        <div class="col-inner card-layout">
          <div>
              <div class="icon-wrapper">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-icon"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>
              </div>
              <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">โปรโมชั่น</h3>
              <p style="font-size: 0.9em; color: #666; line-height: 1.5;">อัปเดตโปรโมชั่นฉีดฟิลเลอร์สะโพก และบริการอื่นๆ ในราคาพิเศษสุดคุ้ม</p>
          </div>
          <div style="margin-top: 15px;">
              <a href="#" class="btn-card">ดูโปรโมชั่น</a>
          </div>
        </div>
      </div>

      <!-- Card 3: Clinic Awards (Swapped) -->
      <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px;">
        <div class="col-inner card-layout">
          <div>
              <div class="icon-wrapper">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-icon"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              </div>
              <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">Clinic Awards</h3>
              <p style="font-size: 0.9em; color: #666; line-height: 1.5;">การันตีคุณภาพด้วยรางวัลระดับประเทศมากมาย มั่นใจในความปลอดภัย 100%</p>
          </div>
          <div style="margin-top: 15px;">
              <a href="#" class="btn-card">ดูรางวัลทั้งหมด</a>
          </div>
        </div>
      </div>

      <!-- Card 4: ติดต่อเรา -->
      <div class="col small-12 medium-6 large-3 text-center" style="padding: 10px;">
        <div class="col-inner card-layout">
          <div>
              <div class="icon-wrapper">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-icon"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              </div>
              <h3 style="color: #154a5c; font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">ติดต่อเรา</h3>
              <p style="font-size: 0.9em; color: #666; line-height: 1.5;">ปรึกษาแพทย์ฟรี ไม่มีค่าใช้จ่าย<br>พร้อมดูแลคุณอย่างใกล้ชิด</p>
          </div>
          <div style="display: flex; justify-content: center; gap: 8px; margin-top: 15px;">
            <a href="https://lin.ee/dyBcDPC" target="_blank" class="btn-social" style="background-color: #00B900; box-shadow: 0 4px 6px rgba(0,185,0,0.3);">LINE</a>
            <a href="https://m.me/102574639184550" target="_blank" class="btn-social" style="background-color: #0084FF; box-shadow: 0 4px 6px rgba(0,132,255,0.3);">Messenger</a>
          </div>
        </div>
      </div>
    </div>
    """
    
    new_soup = BeautifulSoup(new_html, 'html.parser')
    footer.replace_with(new_soup)
    
    # Add CSS for cards
    style_tag = soup.new_tag('style')
    style_tag.string = """
    .card-layout {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    .card-layout:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: #154a5c;
    }
    .icon-wrapper {
        width: 70px;
        height: 70px;
        background-color: #f0f7f9;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
        transition: all 0.3s ease;
    }
    .card-icon {
        color: #154a5c;
        transition: all 0.3s ease;
    }
    .card-layout:hover .icon-wrapper {
        background-color: #154a5c;
    }
    .card-layout:hover .card-icon {
        color: #ffffff;
        stroke: #ffffff;
    }
    .btn-card {
        display: inline-block;
        padding: 8px 20px;
        background-color: transparent;
        color: #154a5c;
        border-radius: 30px;
        text-decoration: none;
        font-size: 0.9em;
        border: 2px solid #154a5c;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .btn-card:hover {
        background-color: #154a5c;
        color: white !important;
    }
    .btn-social {
        display: inline-block;
        padding: 8px 12px;
        color: white !important;
        border-radius: 30px;
        text-decoration: none;
        font-size: 0.85em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .btn-social:hover {
        transform: translateY(-2px);
        opacity: 0.9;
    }
    """
    
    # We might have old styles from earlier, let's just append this new style to head
    soup.head.append(style_tag)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Replaced footer with 4 cards layout.')
else:
    print('Footer not found.')
