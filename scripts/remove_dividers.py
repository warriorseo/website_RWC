import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

count_hr = 0
for hr in soup.find_all('hr'):
    hr.decompose()
    count_hr += 1

count_divider = 0
for divider in soup.find_all('div', class_='divider'):
    # In Flatsome, dividers often have a parent row or col that might be empty if the divider is removed.
    # Let's check if the parent row/col becomes empty and remove it if so.
    parent_col = divider.find_parent('div', class_=lambda c: c and 'col ' in c)
    divider.decompose()
    count_divider += 1
    
    # Optional cleanup of empty columns after divider removal
    if parent_col and not parent_col.get_text(strip=True) and not parent_col.find('img'):
        # If the column only contained the divider, remove the column
        parent_row = parent_col.find_parent('div', class_='row')
        parent_col.decompose()
        if parent_row and not parent_row.find_all(recursive=False):
            # If row is now empty, remove row
            parent_row.decompose()

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print(f'Removed {count_hr} <hr> tags and {count_divider} divider divs.')
