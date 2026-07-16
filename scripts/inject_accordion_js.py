import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

accordion_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var accordions = document.querySelectorAll('.accordion-title');
    accordions.forEach(function(acc) {
        acc.addEventListener('click', function(e) {
            e.preventDefault();
            var item = this.closest('.accordion-item');
            var inner = item.querySelector('.accordion-inner');
            var isActive = item.classList.contains('active');
            var icon = this.querySelector('.simple-toggle');
            
            // Close all others in the same accordion group
            var group = this.closest('.accordion');
            group.querySelectorAll('.accordion-item').forEach(function(i) {
                i.classList.remove('active');
                var innerToClose = i.querySelector('.accordion-inner');
                if(innerToClose) innerToClose.style.display = 'none';
                var iIcon = i.querySelector('.simple-toggle');
                if(iIcon) iIcon.textContent = '+';
            });
            
            // Toggle current
            if (!isActive) {
                item.classList.add('active');
                if(inner) inner.style.display = 'block';
                if(icon) icon.textContent = '-';
            }
        });
    });
});
</script>
"""

# Check if script already exists to prevent duplicate injection
script_exists = soup.find('script', string=re.compile('var accordions = document.querySelectorAll'))
if not script_exists:
    body = soup.find('body')
    if body:
        js_soup = BeautifulSoup(accordion_js, 'html.parser')
        body.append(js_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Injected Accordion JS.')
    else:
        print('Body not found.')
else:
    print('Accordion JS already exists.')
