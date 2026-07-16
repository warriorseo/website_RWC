import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

accordion = soup.find('div', class_='accordion')
if accordion:
    items = accordion.find_all('div', class_='accordion-item')
    for item in items:
        # Find the old button toggle
        btn_toggle = item.find('button', class_='toggle')
        if btn_toggle:
            btn_toggle.decompose()
        
        # Add a simple text icon if not already there
        title_a = item.find('a', class_='accordion-title')
        if title_a:
            if not title_a.find('span', class_='simple-toggle'):
                icon_span = soup.new_tag('span', class_='simple-toggle', style='margin-right: 10px; color: #154a5c; font-weight: bold;')
                icon_span.string = '+'
                title_a.insert(0, icon_span)
                
    # Update the JS
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string and 'accordions.forEach' in script.string:
            script.string = """
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
                            inner.style.display = 'block';
                            if(icon) icon.textContent = '-';
                        }
                    });
                });
            });
            """
            break
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Simplified Accordion toggles.')
else:
    print('Accordion not found.')
