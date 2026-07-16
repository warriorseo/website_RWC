import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

accordion = soup.find('div', class_='accordion')
if accordion:
    js_html = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var accordions = document.querySelectorAll('.accordion-title');
        accordions.forEach(function(acc) {
            acc.addEventListener('click', function(e) {
                e.preventDefault();
                var item = this.closest('.accordion-item');
                var inner = item.querySelector('.accordion-inner');
                var isActive = item.classList.contains('active');
                
                // Close all others in the same accordion group
                var group = this.closest('.accordion');
                group.querySelectorAll('.accordion-item').forEach(function(i) {
                    i.classList.remove('active');
                    var innerToClose = i.querySelector('.accordion-inner');
                    if(innerToClose) innerToClose.style.display = 'none';
                });
                
                // Toggle current
                if (!isActive) {
                    item.classList.add('active');
                    inner.style.display = 'block';
                }
            });
        });
    });
    </script>
    <style>
        .accordion-item.active .accordion-title { color: #154a5c; font-weight: bold; }
        .accordion-item.active .toggle i:before { content: "\\f106"; } /* Assuming FontAwesome is used for up arrow, or it just rotates */
    </style>
    """
    
    # check if already injected
    if not soup.find('script', string=re.compile('accordions.forEach')):
        new_soup = BeautifulSoup(js_html, 'html.parser')
        accordion.insert_after(new_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Injected Accordion JS successfully.')
    else:
        print('Accordion JS already exists.')
else:
    print('Accordion not found.')
