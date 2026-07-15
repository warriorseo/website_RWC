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

# Try to find the main content. Often in <article> or <div class="entry-content">
content = soup.find('article') or soup.find('div', class_='entry-content') or soup.find('main') or soup.body

if not content:
    print("Could not find main content")
    exit(1)

# Remove some unnecessary elements like scripts, styles, header, footer
for element in content(['script', 'style', 'nav', 'noscript', 'iframe']):
    element.decompose()

# Process images
img_tags = content.find_all('img')
for i, img in enumerate(img_tags):
    # Some images might use lazy loading attributes like data-src or data-lazy-src
    img_src = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
    
    if not img_src: continue
    
    if img_src.startswith('data:image'): continue # Skip base64 inline images
    
    # Make absolute URL
    img_url = urllib.parse.urljoin(url, img_src)
    
    # Generate filename
    ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1]
    if not ext: ext = '.jpg'
    
    filename = f'hip_filler_{i}{ext}'
    filepath = os.path.join(images_dir, filename)
    
    print(f"Downloading {img_url} to {filename}...")
    try:
        img_res = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        if img_res.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(img_res.content)
            # Update src in HTML
            img['src'] = f'images/{filename}'
            
            # Remove srcset and sizes so browser doesn't try to load them
            for attr in ['srcset', 'data-srcset', 'sizes', 'data-sizes']:
                if attr in img.attrs:
                    del img[attr]
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

html_output_path = os.path.join(output_dir, 'hip_filler_injection.html')

html_template = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hip Filler Injection - Extracted Content</title>
    <style>
        body {{ font-family: 'Sarabun', sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    {content.prettify()}
</body>
</html>
"""

with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Successfully saved HTML to {html_output_path}")
