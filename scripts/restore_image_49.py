import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

footer = soup.find('div', id='row-footer-4-columns')
if footer:
    img_html = """
    <div class="row" style="margin-bottom: 20px;">
     <div class="col small-12 large-12" style="text-align: center;">
      <a href="https://rwcclinic.com/dr-kanom-rwc/">
       <img alt="หมอขนม RWC Clinic" src="images/hip_filler_49.jpg" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"/>
      </a>
     </div>
    </div>
    """
    img_soup = BeautifulSoup(img_html, 'html.parser')
    footer.insert_before(img_soup)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Restored image 49 above the 4 columns.')
else:
    print('Footer not found.')
