import csv
import re
import requests
from requests.auth import HTTPBasicAuth

CSV_FILE = r"d:\AI-Cyborg-2558\_SEO_Clients\RWC\sheet_data.csv"
WP_USER = "seo@warrior.in.th"
WP_PASS = "tl50 hSv5 56Mq 2iEQ qTMu X8Jy"
WP_BASE = "https://rwcclinic.com/wp-json/wp/v2"

urls_to_check = [
    "https://rwcclinic.com/filler-injection-expert/",
    "https://rwcclinic.com/filler-under-eyes/",
    "https://rwcclinic.com/forehead-filler-injection/",
    "https://rwcclinic.com/temple-filler/",
    "https://rwcclinic.com/nose-filler-injection/",
    "https://rwcclinic.com/filler-cheek-groove/",
    "https://rwcclinic.com/lips-filler/",
    "https://rwcclinic.com/chin-filler/",
    "https://rwcclinic.com/vagina-filler/",
    "https://rwcclinic.com/hip-filler-injection/",
    "https://rwcclinic.com/breaking-down-fillers/",
    "https://rwcclinic.com/cheek-filler/" 
]

pages_data = {}
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        url = row[0]
        if url in urls_to_check and len(row) > 11:
            col_l = row[11]
            lines = col_l.split('\n')
            
            a_val, t_val, e_val = "N/A", "N/A", "N/A"
            a_curr = "0"
            
            if len(lines) >= 3:
                match_a = re.search(r'A:([+-]?\d+)%', lines[-1])
                match_t = re.search(r'T:([+-]?\d+)%', lines[-1])
                match_e = re.search(r'E:([+-]?\d+)%', lines[-1])
                if match_a: a_val = match_a.group(1) + "%"
                if match_t: t_val = match_t.group(1) + "%"
                if match_e: e_val = match_e.group(1) + "%"
                
                match_a_curr = re.search(r'A:(\d+)', lines[0])
                if match_a_curr: a_curr = match_a_curr.group(1)
                
            pages_data[url] = {
                'active_users': a_curr,
                'a_drop': a_val,
                't_drop': t_val,
                'e_drop': e_val
            }

auth = HTTPBasicAuth(WP_USER, WP_PASS)

for url in urls_to_check:
    slug = url.strip('/').split('/')[-1]
    if not slug: continue
    
    print(f"Checking {url}...")
    try:
        res = requests.get(f"{WP_BASE}/pages?slug={slug}", auth=auth, timeout=5)
        data = res.json()
        post_type = 'pages'
        
        if not data or not isinstance(data, list) or len(data) == 0:
            res = requests.get(f"{WP_BASE}/posts?slug={slug}", auth=auth, timeout=5)
            if res.status_code == 200:
                data = res.json()
            post_type = 'posts'
            
        if not data or not isinstance(data, list) or len(data) == 0:
            print(f"  Not found in WP.")
            continue
            
        post_id = data[0].get('id')
        
        rev_res = requests.get(f"{WP_BASE}/{post_type}/{post_id}/revisions", auth=auth, timeout=5)
        if rev_res.status_code == 200:
            rev_data = rev_res.json()
            rev_dates = [r['date'] for r in rev_data]
            pd = pages_data.get(url, {})
            print(f"  Traffic: {pd.get('active_users')} | YoY T Drop: {pd.get('t_drop')} | Total Revisions: {len(rev_dates)}")
            for rev in rev_dates[:3]:
                print(f"    - {rev}")
        else:
            print(f"  Error fetching revisions: {rev_res.status_code}")
    except Exception as e:
        print(f"  Exception: {e}")
