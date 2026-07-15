from bs4 import BeautifulSoup
import os

filepath = r'd:\AI-Cyborg-2558\_SEO_Clients\RWC\web\hip_filler_injection.html'

with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find accordion
accordion = soup.find('div', class_='accordion')
if accordion:
    # Get the title
    title_span = accordion.find('span', string=lambda t: t and 'สารบัญ' in t)
    title_text = title_span.text if title_span else "สารบัญ"
    
    new_title = soup.new_tag('h2')
    new_title['style'] = 'color: #154a5c;'
    new_title.string = title_text
    
    # Get the inner content
    inner = accordion.find('div', class_='accordion-inner')
    
    if inner:
        new_div = soup.new_tag('div')
        new_div['style'] = 'background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #eee;'
        
        # Add title
        new_div.append(new_title)
        
        # Add contents
        for child in inner.contents[:]:
            new_div.append(child)
            
        accordion.replace_with(new_div)
        print("TOC expanded successfully.")
    else:
        print("Could not find accordion-inner")
else:
    print("No accordion found.")

# Save modified HTML
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
