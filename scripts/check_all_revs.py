import requests
from requests.auth import HTTPBasicAuth
WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)
slug = 'nose-filler-injection'
res = requests.get(f'{WP_BASE}/pages?slug={slug}', auth=auth)
data = res.json()
if not data:
    res = requests.get(f'{WP_BASE}/posts?slug={slug}', auth=auth)
    data = res.json()
post_type = 'pages' if 'pages' in res.url else 'posts'
post_id = data[0]['id']
page = 1
while True:
    r = requests.get(f'{WP_BASE}/{post_type}/{post_id}/revisions?per_page=100&page={page}', auth=auth)
    if r.status_code != 200: break
    revs = r.json()
    if not revs: break
    for rev in revs: print(rev['date'])
    page += 1
