from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target_h2 = None
for h in soup.find_all('h2'):
    if 'เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร' in h.get_text():
        target_h2 = h
        break

if target_h2:
    parent_row = target_h2.find_next_sibling('div', class_='row')
    if parent_row:
        new_mockup = """
        <div class="row" style="margin-bottom: 40px; margin-top: 20px;">
            <div class="col small-12 large-12">
                
                <!-- 1. Intro Paragraph -->
                <p style="font-size: 1.1em; color: #555; text-align: center; margin-bottom: 20px;">
                    [Mockup Paragraph: บทนำสั้นๆ เกริ่นถึงความเจ็บปวดจากการผ่าตัด และความสะดวกสบายของการฉีดฟิลเลอร์ที่ตอบโจทย์กว่า]
                </p>
                
                <!-- 2. Image Placeholder (Between Paragraph and Table) -->
                <div style="background-color: #f1f1f1; height: 350px; max-width: 800px; margin: 0 auto 30px auto; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 2px dashed #bbb;">
                    <span style="color: #666; font-size: 1.2em; font-weight: bold; text-align: center;">
                        📸 [Mockup Image: ภาพ Infographic เปรียบเทียบฟิลเลอร์ vs ซิลิโคน]<br>
                        <span style="font-size: 0.8em; font-weight: normal;">(ภาพควรวางอยู่ใต้ Paragraph เพื่อดึงดูดสายตาก่อนลงลึกที่ตาราง)</span>
                    </span>
                </div>
                
                <!-- 3. Table Mockup -->
                <div style="max-width: 800px; margin: 0 auto;">
                    <h3 style="color: #154a5c; text-align: center; margin-bottom: 15px;">ตารางเปรียบเทียบข้อแตกต่าง</h3>
                    <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 1em;">
                        <thead>
                            <tr style="background-color: #154a5c; color: white;">
                                <th style="padding: 15px; border: 1px solid #ddd; width: 33%;">หัวข้อเปรียบเทียบ</th>
                                <th style="padding: 15px; border: 1px solid #ddd; width: 33%;">ฉีดฟิลเลอร์สะโพก ✨</th>
                                <th style="padding: 15px; border: 1px solid #ddd; width: 33%;">ผ่าตัดเสริมซิลิโคน</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="background-color: #f9f9f9;">
                                <td style="padding: 15px; border: 1px solid #ddd; font-weight: bold;">[Mockup: ความเจ็บปวด]</td>
                                <td style="padding: 15px; border: 1px solid #ddd; color: #25d366;">[Mockup: เจ็บน้อยมาก]</td>
                                <td style="padding: 15px; border: 1px solid #ddd; color: #da0000;">[Mockup: เจ็บมาก]</td>
                            </tr>
                            <tr>
                                <td style="padding: 15px; border: 1px solid #ddd; font-weight: bold;">[Mockup: ระยะเวลาพักฟื้น]</td>
                                <td style="padding: 15px; border: 1px solid #ddd;">[Mockup: ไม่ต้องพักฟื้น]</td>
                                <td style="padding: 15px; border: 1px solid #ddd;">[Mockup: 1-2 เดือน]</td>
                            </tr>
                            <tr style="background-color: #f9f9f9;">
                                <td style="padding: 15px; border: 1px solid #ddd; font-weight: bold;">[Mockup: สัมผัส]</td>
                                <td style="padding: 15px; border: 1px solid #ddd;">[Mockup: นิ่มเป็นธรรมชาติ]</td>
                                <td style="padding: 15px; border: 1px solid #ddd;">[Mockup: อาจจับเป็นก้อนแข็ง]</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
        """
        new_soup = BeautifulSoup(new_mockup, 'html.parser')
        parent_row.replace_with(new_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Injected Table Mockup and restructured layout.')
    else:
        print('Parent row not found.')
else:
    print('H2 not found.')
