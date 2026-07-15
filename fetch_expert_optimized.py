import requests
from requests.auth import HTTPBasicAuth
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

post_type = 'pages' if 'pages' in res.url else 'posts'
post_id = data[0]['id']

page = 1
done = False
print('Revisions from April 2026 to present:')
while not done:
    revs = requests.get(f'{WP_BASE}/{post_type}/{post_id}/revisions?per_page=100&page={page}', auth=auth).json()
    if not revs or isinstance(revs, dict) and 'code' in revs:
        break
    for rev in revs:
        if rev['date'] < '2026-04-01':
            done = True
            break
        print(f"- {rev['date']}")
    page += 1
