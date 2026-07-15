from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')
awards_container = content.contents[107]

# Define the new mockup section
new_section = BeautifulSoup("""
<div class="row" style="margin-bottom: 30px; margin-top: 30px; background-color: #f9f9f9; padding: 30px; border-radius: 12px; border: 1px solid #eee;">
    <div class="col small-12 large-12" style="text-align: center;">
        <!-- Mockup Data Placeholder Image -->
        <div style="background-color: #e0e0e0; height: 300px; max-width: 800px; margin: 0 auto 20px auto; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 2px dashed #999;">
            <span style="color: #555; font-size: 20px; font-weight: bold;">[ภาพ Mockup Data: รวมรางวัล RWC Clinic]</span>
        </div>
        <h3 style="color: #154a5c; font-size: 1.5em; margin-bottom: 10px;">RWC Clinic รับ 2 รางวัลสุดยิ่งใหญ่ ระดับประเทศ ประจำปี 2023-2024</h3>
        <p style="font-size: 1.1em; color: #333; max-width: 800px; margin: 0 auto 20px auto;">
            การันตีคุณภาพด้วยรางวัล <strong>แพทย์ที่มีเทคนิคการฉีดฟิลเลอร์โดดเด่นของประเทศไทย</strong> (New Star Awards) และ <strong>คลินิกที่ฉีดฟิลเลอร์สะโพกสูงสุดในประเทศไทย</strong> (Gluteal Augment Leader)
        </p>
        <p>
            <a href="https://rwcclinic.com/our-awards/" target="_blank" style="display: inline-block; background-color: #d83131; color: #fff; padding: 10px 25px; border-radius: 5px; font-weight: bold; text-decoration: none;">
                🏆 ดูความสำเร็จและรางวัลทั้งหมดของเรา คลิกที่นี่
            </a>
        </p>
    </div>
</div>
""", 'html.parser')

# Replace the old container with the new one
awards_container.replace_with(new_section)
print("Replaced Awards section with Mockup Data and Internal Link.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
