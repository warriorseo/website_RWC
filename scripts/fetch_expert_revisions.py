import requests
import json
from requests.auth import HTTPBasicAuth

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

slug = 'filler-injection-expert'
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
    print(f'Found {len(revs)} revisions.')
    
    # Save the first 3 revisions for analysis
    for idx, r in enumerate(revs[:3]):
        with open(f'd:\\AI-Cyborg-2558\\_SEO_Clients\\RWC\\revision_{idx}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Date: {r['date']}\n")
            f.write(f"Content:\n{r['content']['rendered']}\n")
            
    print('Saved top 3 revisions.')
else:
    print('Page not found')
