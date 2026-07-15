from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

wrapper = soup.find('div', class_='steps-carousel-wrapper')
if wrapper:
    # We will rebuild just the inner slider HTML
    slider = wrapper.find('div', class_=lambda c: c and 'slider' in c and not 'slider-wrapper' in c)
    if slider:
        slides = slider.find_all('div', class_=lambda c: c and 'col ' in c, recursive=False)
        
        # Build the correct Flatsome Row Slider HTML
        new_slider_html = """
        <div class="row slider slider-nav-circle slider-nav-large slider-style-normal" data-flickity-options='{"cellAlign": "center", "imagesLoaded": true, "wrapAround": true, "autoPlay": 6000, "pageDots": true, "prevNextButtons": true}'>
        """
        for slide in slides:
            # Add w-100 to force slide width
            new_slider_html += f'<div class="col small-12 large-12" style="width: 100%;">{slide.decode_contents()}</div>'
        new_slider_html += '</div>'
        
        new_slider_soup = BeautifulSoup(new_slider_html, 'html.parser')
        
        # Replace the old <div class="row"> inside the wrapper with just the new row slider
        old_row = wrapper.find('div', class_='row')
        if old_row:
            old_row.replace_with(new_slider_soup)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Fixed carousel structure.')
    else:
        print('Slider not found.')
else:
    print('Wrapper not found.')
