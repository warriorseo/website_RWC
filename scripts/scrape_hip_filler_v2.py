import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re

url = 'https://rwcclinic.com/hip-filler-injection/'
output_dir = r'd:\AI-Cyborg-2558\_SEO_Clients\RWC\web'
images_dir = os.path.join(output_dir, 'images')

os.makedirs(images_dir, exist_ok=True)

print(f"Fetching {url}...")
res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
res.raise_for_status()

soup = BeautifulSoup(res.text, 'html.parser')

# Get all stylesheets and styles from the original head
head_styles = []
for tag in soup.head.find_all(['link', 'style']):
    # Remove lazy load CSS that hides images
    if tag.name == 'style' and 'rocket-lazyload' in tag.get('id', ''):
        continue
    
    if tag.name == 'style':
        head_styles.append(str(tag))
    elif tag.name == 'link' and tag.get('rel') == ['stylesheet']:
        # Make href absolute
        href = tag.get('href')
        if href:
            tag['href'] = urllib.parse.urljoin(url, href)
            head_styles.append(str(tag))
            
# Try to find the main content.
content = soup.find('div', class_='entry-content') or soup.find('main') or soup.find('article') or soup.body

if not content:
    print("Could not find main content")
    exit(1)

# Remove scripts to avoid execution, but keep styles
for element in content(['script', 'noscript', 'iframe']):
    element.decompose()

# Process images
img_tags = content.find_all('img')
for i, img in enumerate(img_tags):
    img_src = img.get('data-lazy-src') or img.get('src')
    if not img_src or img_src.startswith('data:image'): continue
    
    img_url = urllib.parse.urljoin(url, img_src)
    ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1]
    if not ext: ext = '.jpg'
    
    filename = f'hip_filler_{i}{ext}'
    filepath = os.path.join(images_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Downloading {img_url} to {filename}...")
        try:
            img_res = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            if img_res.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(img_res.content)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            
    # Update src in HTML
    img['src'] = f'images/{filename}'
    
    # Remove lazy loading attributes that might conflict with CSS hiding them
    for attr in ['srcset', 'data-srcset', 'sizes', 'data-sizes', 'loading', 'decoding', 'data-lazy-src', 'data-lazy-sizes']:
        if attr in img.attrs:
            del img[attr]

html_output_path = os.path.join(output_dir, 'hip_filler_injection.html')

html_template = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hip Filler Injection - Original Styling</title>
    {''.join(head_styles)}
    <style>
        /* Force body to be white in case original css assumes a wrapper background */
        body {{ background-color: #fff; margin: 0; padding: 0; }}
        /* Adjust wrapper width to match typical Flatsome desktop container */
        #content-wrapper {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
    </style>
</head>
<body>
    <div id="content-wrapper">
        {content.prettify()}
    </div>
</body>
</html>
"""

with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Successfully saved HTML to {html_output_path}")
