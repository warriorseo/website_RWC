import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Check if lightbox JS already exists
if not soup.find('script', string=re.compile('mock-lightbox')):
    lightbox_html = """
    <div id="mock-lightbox" style="display:none; position:fixed; z-index:9999; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); align-items:center; justify-content:center; cursor:zoom-out;">
        <img id="mock-lightbox-img" src="" style="max-width:90%; max-height:90%; object-fit:contain; border-radius:8px; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var links = document.querySelectorAll('.image-lightbox');
        var lightbox = document.getElementById('mock-lightbox');
        var lightboxImg = document.getElementById('mock-lightbox-img');
        
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                lightboxImg.src = this.getAttribute('href');
                lightbox.style.display = 'flex';
            });
        });
        
        lightbox.addEventListener('click', function() {
            lightbox.style.display = 'none';
            lightboxImg.src = '';
        });
    });
    </script>
    """
    
    body = soup.find('body')
    if body:
        new_soup = BeautifulSoup(lightbox_html, 'html.parser')
        body.append(new_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Injected Mock Lightbox JS.')
    else:
        print('Body tag not found.')
else:
    print('Lightbox JS already injected.')
