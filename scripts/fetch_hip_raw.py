import requests
from requests.auth import HTTPBasicAuth
import json

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

post_id = 47343

# Get current content
r = requests.get(f'{WP_BASE}/pages/{post_id}?context=edit', auth=auth)
data = r.json()

if 'content' in data:
    with open('hip_content_raw.txt', 'w', encoding='utf-8') as f:
        f.write(data['content']['raw'])
    print("Saved raw content to hip_content_raw.txt")
else:
    print("Could not fetch content", data)
