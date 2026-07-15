from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

award_heading = soup.find(string=re.compile('รับ 2 รางวัลสุดยิ่งใหญ่'))
if award_heading:
    parent_row = award_heading.find_parent('div', class_='row')
    if parent_row:
        # Find the anchor tag inside this row
        a_tag = parent_row.find('a', href=True)
        if a_tag:
            a_tag['href'] = "https://rwcclinic.com/trophy/"
            a_tag.string = "ดูรางวัลระดับประเทศทั้งหมด"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print('Award link updated successfully.')
        else:
            print('Could not find anchor tag in Award section.')
else:
    print('Award section not found.')
