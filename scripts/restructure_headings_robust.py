from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

def robust_find_h2(text_to_find):
    for h2 in soup.find_all('h2'):
        if text_to_find in h2.get_text():
            return h2
    return None

h2_1 = robust_find_h2('ฟิลเลอร์สะโพก คืออะไร')
if h2_1:
    h2_1.string = "เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร"
    print("Updated H2: 'คืออะไร'")

h2_2 = robust_find_h2('ฟิลเลอร์สะโพก ดีอย่างไร')
if h2_2:
    h2_2.decompose()
    print("Removed H2: 'ดีอย่างไร' (Merged sections)")

h2_3 = robust_find_h2('เหมาะกับใครบ้าง')
if h2_3:
    h2_3.string = "เช็กลิสต์: คุณเหมาะกับการปั้นสะโพกด้วยฟิลเลอร์หรือไม่?"
    print("Updated H2: 'เหมาะกับใครบ้าง'")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("Saved HTML.")
