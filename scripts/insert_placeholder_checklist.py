from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find the heading
h2 = soup.find('h2', string=re.compile('เช็กลิสต์: คุณเหมาะกับการปั้นสะโพกด้วยฟิลเลอร์หรือไม่'))
if h2:
    # Find the paragraph immediately following it
    p = h2.find_next_sibling('p')
    if p and 'เหมาะกับใครบ้าง' in p.get_text():
        # Replace the paragraph with a placeholder checklist
        mockup_checklist = BeautifulSoup('''
        <p style="color: #666; font-style: italic;">[ทีมลูกค้า: กรุณาใส่เนื้อหาเช็กลิสต์ตรงนี้ (เช่น 3-5 ข้อ) เพื่อให้อ่านง่ายและกระชับ]</p>
        <ul style="color: #666; background-color: #f9f9f9; padding: 20px 40px; border-radius: 8px; border: 1px dashed #ccc;">
            <li>[ข้อ 1: เช่น คนที่กลัวการผ่าตัดศัลยกรรม ไม่มีเวลาพักฟื้น]</li>
            <li>[ข้อ 2: เช่น คนที่มีปัญหาสะโพกบุ๋ม สะโพกแหว่ง ต้องการเติมเต็มให้กลมกลึง]</li>
            <li>[ข้อ 3: เช่น ผู้ที่ต้องการเห็นผลลัพธ์ทันทีหลังทำ]</li>
            <li>[ข้อ 4: ใส่ข้อความเพิ่มเติม...]</li>
        </ul>
        ''', 'html.parser')
        p.replace_with(mockup_checklist)
        print("Replaced text with Mockup Checklist.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("Saved HTML.")
