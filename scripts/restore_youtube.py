import requests
from bs4 import BeautifulSoup
import re

# 1. Fetch live HTML and extract video containers
print("Fetching live HTML...")
res = requests.get('https://rwcclinic.com/hip-filler-injection/', headers={'User-Agent': 'Mozilla/5.0'})
live_soup = BeautifulSoup(res.text, 'html.parser')
live_videos = live_soup.find_all('div', class_='video video-fit mb')
print(f"Found {len(live_videos)} video containers in live HTML.")

# 2. Open local HTML
local_path = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(local_path, 'r', encoding='utf-8') as f:
    local_soup = BeautifulSoup(f.read(), 'html.parser')

local_videos = local_soup.find_all('div', class_='video video-fit mb')
print(f"Found {len(local_videos)} video containers in local HTML.")

# 3. Inject live video contents into local video containers
if len(live_videos) == len(local_videos):
    for live_vid, local_vid in zip(live_videos, local_videos):
        # Clear local video contents (the <p> tag)
        local_vid.clear()
        # Append contents from live video
        for child in live_vid.contents:
            # We must copy the tag to avoid removing it from live_vid and messing up iterators
            from copy import copy
            local_vid.append(copy(child))
    print("Injected iframes successfully.")
else:
    print("Warning: Mismatch in video count! Injecting based on zip...")
    for live_vid, local_vid in zip(live_videos, local_videos):
        local_vid.clear()
        from copy import copy
        for child in live_vid.contents:
            local_vid.append(copy(child))

# 4. Move the specific video to the top
print("Moving target video row...")
# Find the specific heading "เรื่องต้องรู้ก่อนฉีดฟิลเลอร์สะโพก"
target_heading = local_soup.find(string=re.compile('เรื่องต้องรู้ก่อนฉีดฟิลเลอร์สะโพก'))
if target_heading:
    target_row = target_heading.find_parent('div', class_='row')
    
    # Find TOC container to insert after it
    toc_text = local_soup.find(string=re.compile('สารบัญฟิลเลอร์สะโพก'))
    if toc_text:
        content = local_soup.find('div', class_='content-area')
        toc_container = toc_text
        while toc_container and toc_container.parent != content:
            toc_container = toc_container.parent
        
        if target_row and toc_container:
            target_row.extract()
            toc_container.insert_after(target_row)
            print("Moved target video row successfully.")
        else:
            print("Could not find target_row or toc_container top level.")
    else:
        print("TOC not found.")
else:
    print("Target video heading not found.")

# 5. Save the updated HTML
with open(local_path, 'w', encoding='utf-8') as f:
    f.write(local_soup.prettify())
print("Saved local HTML.")
