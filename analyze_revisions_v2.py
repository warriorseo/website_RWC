import csv
import re
import requests
from requests.auth import HTTPBasicAuth

CSV_FILE = r"d:\AI-Cyborg-2558\_SEO_Clients\RWC\sheet_data.csv"
WP_USER = "seo@warrior.in.th"
WP_PASS = "tl50 hSv5 56Mq 2iEQ qTMu X8Jy"
WP_BASE = "https://rwcclinic.com/wp-json/wp/v2"

pages_to_check = []
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        if len(row) > 11:
            url = row[0]
            col_l = row[11]
            if "T:-" in col_l and "A:" in col_l:
                lines = col_l.split('\n')
                if len(lines) >= 3:
                    # lines[0] is current year, lines[1] is previous year, lines[2] is YoY diff
                    # e.g., A:875 | T:30s | E:34%
                    match_a = re.search(r'A:(\d+)', lines[0])
                    match_t_drop = re.search(r'T:-(\d+)%', lines[-1])
                    
                    if match_a and match_t_drop:
                        active_users = int(match_a.group(1))
                        drop = int(match_t_drop.group(1))
                        
                        # Filter for high traffic pages with significant drops
                        if active_users > 100 and drop >= 20:
                            pages_to_check.append({'url': url, 'active_users': active_users, 'drop': drop})

# Sort by drop %
pages_to_check = sorted(pages_to_check, key=lambda x: x['drop'], reverse=True)
pages_to_check = pages_to_check[:15]

results = []
auth = HTTPBasicAuth(WP_USER, WP_PASS)

print(f"Checking {len(pages_to_check)} significant pages...")

for page in pages_to_check:
    url = page['url']
    slug = url.strip('/').split('/')[-1] if url.strip('/') else ''
    if not slug:
        continue
    
    # Try page first
    res = requests.get(f"{WP_BASE}/pages?slug={slug}", auth=auth)
    data = res.json()
    post_type = 'pages'
    
    if not data or not isinstance(data, list) or len(data) == 0:
        # Try post
        res = requests.get(f"{WP_BASE}/posts?slug={slug}", auth=auth)
        if res.status_code == 200:
            data = res.json()
        post_type = 'posts'
        
    if not data or not isinstance(data, list) or len(data) == 0:
        print(f"Could not find ID for {url}")
        results.append({'url': url, 'drop': page['drop'], 'users': page['active_users'], 'revisions': [], 'error': 'Not found'})
        continue
        
    post_id = data[0].get('id')
    if not post_id:
        continue
    
    # Fetch revisions
    rev_res = requests.get(f"{WP_BASE}/{post_type}/{post_id}/revisions", auth=auth)
    if rev_res.status_code == 200:
        rev_data = rev_res.json()
        rev_dates = [r['date'] for r in rev_data]
        results.append({'url': url, 'drop': page['drop'], 'users': page['active_users'], 'revisions': rev_dates})
    else:
        results.append({'url': url, 'drop': page['drop'], 'users': page['active_users'], 'revisions': [], 'error': f"{rev_res.status_code} {rev_res.text}"})

with open(r"d:\AI-Cyborg-2558\_SEO_Clients\RWC\revision_results_v2.txt", "w", encoding='utf-8') as f:
    for r in results:
        f.write(f"URL: {r['url']} (Engagement Time Drop: {r['drop']}%, Active Users: {r['users']})\n")
        if 'error' in r:
            f.write(f"  Error: {r['error']}\n")
        else:
            f.write(f"  Total Revisions: {len(r['revisions'])}\n")
            for rev in r['revisions'][:5]:
                f.write(f"    - {rev}\n")
        f.write("\n")
print("Done. Saved to revision_results_v2.txt")
