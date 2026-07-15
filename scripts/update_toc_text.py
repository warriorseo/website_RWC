from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

toc_heading = soup.find(string=re.compile('สารบัญฟิลเลอร์สะโพก'))
if toc_heading:
    # Use replace_with to change the text node
    toc_heading.replace_with('สารบัญเนื้อหา')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Updated TOC heading to 'สารบัญเนื้อหา'.")
else:
    print("TOC heading not found.")
