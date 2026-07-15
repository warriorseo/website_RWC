import requests
from requests.auth import HTTPBasicAuth
import json
import re

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)
post_id = 47343

with open('hip_content_raw.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Paolo Hospital link
paolo_pattern = r'<p><a href="https://www\.paolohospital\.com/th-TH/rangsit/Clinic/Details/%E0%B8%A8%E0%B8%B1%E0%B8%A5%E0%B8%A2%E0%B8%81%E0%B8%A3%E0%B8%A3%E0%B8%A1"[^>]*>อ่านเพิ่มเติม</a></p>'
content = re.sub(paolo_pattern, '', content)

# 2. Extract and remove TikTok link
tiktok_str = '<span style="font-size: 100%;"><a class="uppercase" href="https://vt.tiktok.com/ZSrcyXbXg/"><span style="color: #003366;"><strong>&gt;&gt;&gt; ดูรีวิวจาก Influencer ที่มีชื่อเสียงของเราได้ ที่นี่! &lt;&lt;&lt;</strong></span></a></span>'

if tiktok_str in content:
    # Remove from top
    content = content.replace(tiktok_str, '')
    
    # Clean up the `<br />\n</span>` that was before it if it's there
    content = content.replace('<br />\n</span></p>', '</span></p>')
    
    # Append it to the bottom, right before บทสรุป
    tiktok_insert = f'<p style="text-align: center;">{tiktok_str}</p>\n'
    
    conclusion_str = '<h2><strong><span style="color: #154a5c;">บทสรุป</span></strong></h2>'
    content = content.replace(conclusion_str, tiktok_insert + conclusion_str)
else:
    print("Could not find exact TikTok string.")

# Save modified content locally for safety
with open('hip_content_updated.txt', 'w', encoding='utf-8') as f:
    f.write(content)

# Update post via API
data = {'content': content}
res = requests.post(f'{WP_BASE}/pages/{post_id}', auth=auth, json=data)

if res.status_code in [200, 201]:
    print("Successfully updated the page!")
else:
    print(f"Failed to update page: {res.status_code}")
    print(res.text)
