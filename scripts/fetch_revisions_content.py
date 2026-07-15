import requests
import json
import os
from requests.auth import HTTPBasicAuth

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

targets = ['breaking-down-fillers', 'filler-cheek-groove']
output_dir = r'd:\AI-Cyborg-2558\_SEO_Clients\RWC\revisions_html'
os.makedirs(output_dir, exist_ok=True)

for slug in targets:
    print(f"Fetching {slug}...")
    res = requests.get(f'{WP_BASE}/pages?slug={slug}', auth=auth)
    data = res.json()
    if not data:
        res = requests.get(f'{WP_BASE}/posts?slug={slug}', auth=auth)
        data = res.json()
        
    if data:
        post_type = 'pages' if 'pages' in res.url else 'posts'
        post_id = data[0]['id']
        revs = requests.get(f'{WP_BASE}/{post_type}/{post_id}/revisions', auth=auth).json()
        print(f"Found {len(revs)} revisions for {slug}.")
        
        # Save the top 2 revisions
        for i, rev in enumerate(revs[:2]):
            date_str = rev['date'].replace(':', '-')
            file_name = f"{slug}_rev_{i}_{date_str}.html"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(rev['content']['rendered'])
            print(f"Saved {file_name}")
    else:
        print(f"Page {slug} not found.")

print("Done.")
