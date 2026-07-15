from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find the awards link
awards_link = soup.find('a', href='https://rwcclinic.com/our-awards/')
if awards_link:
    awards_link.string = "RWC Awards"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Updated button text to 'RWC Awards'.")
else:
    print("Awards link not found.")
