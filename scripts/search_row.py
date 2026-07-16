import re
from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print('All IDs containing row or 210:')
for tag in soup.find_all(id=True):
    if '210' in tag['id'] or 'row' in tag['id']:
        print(f"{tag.name}: {tag['id']}")
        
print('Scripts:')
for tag in soup.find_all('script'):
    if tag.string and 'row-' in tag.string:
        print('Found script with row-: ', tag.string[:100])
