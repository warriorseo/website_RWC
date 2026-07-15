import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

slug = 'filler-injection-expert'
res = requests.get(f'{WP_BASE}/pages?slug={slug}', auth=auth)
data = res.json()
if not data:
    res = requests.get(f'{WP_BASE}/posts?slug={slug}', auth=auth)
    data = res.json()

if data:
    post_type = 'pages' if 'pages' in res.url else 'posts'
    post_id = data[0]['id']
    
    all_revs = []
    page = 1
    while True:
        rev_url = f'{WP_BASE}/{post_type}/{post_id}/revisions?per_page=100&page={page}'
        r = requests.get(rev_url, auth=auth)
        if r.status_code != 200:
            break
        revs = r.json()
        if not revs:
            break
        all_revs.extend(revs)
        page += 1

    print(f'Total Revisions fetched: {len(all_revs)}')
    print('Revisions from April 2026 to present:')
    
    for rev in all_revs:
        rev_date = rev['date']
        if rev_date >= '2026-04-01':
            print(f"- Revision ID: {rev['id']} on Date: {rev_date}")
