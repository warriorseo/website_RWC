from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

iframes = soup.find_all('iframe')
count = 0
for iframe in iframes:
    lazy_src = iframe.get('data-lazy-src')
    if lazy_src:
        iframe['src'] = lazy_src
        del iframe['data-lazy-src']
        count += 1
        
    # Also clean up WP Rocket classes if any
    if 'data-rocket-lazyload' in iframe.attrs:
        del iframe['data-rocket-lazyload']

print(f"Fixed {count} lazy-loaded iframes.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
