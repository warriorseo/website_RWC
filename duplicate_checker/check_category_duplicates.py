import os
import sys
import requests
import urllib3
import re
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from bs4 import MarkupResemblesLocatorWarning
from pythainlp.tokenize import word_tokenize

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load global .env for GA4 credentials
load_dotenv(r"d:\AI-Cyborg-2558\00_agents\.env")

# Load credentials from wp_credentials.env in parent directory
env_path = os.path.join(os.path.dirname(__file__), '..', 'wp_credentials.env')
env_vars = {}
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                key, val = line.strip().split('=', 1)
                env_vars[key] = val.strip('"\'')
except FileNotFoundError:
    print(f"Error: Credentials file not found at {env_path}")
    sys.exit(1)

WP_USER = env_vars.get("WP_REST_USER")
WP_PASS = env_vars.get("WP_REST_PASS")
BASE_URL = env_vars.get("WP_REST_BASE_URL")

GA4_PROPERTY_ID = "292925407"

def get_ga4_client():
    private_key = os.environ.get("GOOGLE_PRIVATE_KEY", "")
    if "\\n" in private_key:
        private_key = private_key.replace("\\n", "\n")

    credentials_info = {
        "type": os.environ.get("GOOGLE_SERVICE_ACCOUNT_TYPE"),
        "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
        "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
        "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
    }

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    return BetaAnalyticsDataClient(credentials=credentials)

def fetch_ga4_data_1year():
    print("Fetching GA4 data for the last 365 days...")
    client = get_ga4_client()
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="userEngagementDuration"),
            Metric(name="engagementRate")
        ],
        date_ranges=[DateRange(start_date="365daysAgo", end_date="today")],
        limit=100000
    )
    
    response = client.run_report(request)
    ga4_data = {}
    for row in response.rows:
        path = row.dimension_values[0].value
        # Ensure path ends with slash to match WP links consistently, or strip it
        path = path.rstrip('/') + '/'
        
        active_users = int(row.metric_values[0].value)
        engagement_duration = float(row.metric_values[1].value)
        eng_rate = float(row.metric_values[2].value)
        
        avg_time = engagement_duration / active_users if active_users > 0 else 0
        
        ga4_data[path] = {
            'activeUsers': active_users,
            'avgEngagementTime': avg_time,
            'engagementRate': eng_rate
        }
    print(f"Retrieved GA4 data for {len(ga4_data)} pages.")
    return ga4_data

def count_thai_words(text):
    words = word_tokenize(text, engine="newmm", keep_whitespace=False)
    # simple heuristic: if it contains Thai characters, count it
    thai_words = [w for w in words if re.search(r'[\u0E00-\u0E7F]', w)]
    return len(thai_words)

def main():
    parser = argparse.ArgumentParser(description="Check internal duplicate content in a specific WordPress category.")
    parser.add_argument('--category', type=str, required=True, help="Category slug or name to search for (e.g., 'filler', 'surgery')")
    parser.add_argument('--threshold', type=float, default=0.60, help="Similarity threshold (0.0 to 1.0). Default is 0.60 (60%).")
    parser.add_argument('--output', type=str, help="Path to output HTML report (e.g., ../web/duplicate_report.html)")
    args = parser.parse_args()

    search_term = args.category
    threshold = args.threshold

    print(f"Searching for category matching: '{search_term}'...")
    cat_response = requests.get(
        f"{BASE_URL}/categories?search={search_term}",
        auth=(WP_USER, WP_PASS),
        verify=False
    )
    
    if cat_response.status_code != 200:
        print(f"Error fetching categories: {cat_response.text}")
        sys.exit(1)

    cats = cat_response.json()
    if not cats:
        print(f"No category found matching '{search_term}'.")
        sys.exit(1)

    # We take the first match
    target_cat_id = cats[0]['id']
    cat_name = cats[0]['name']
    print(f"Found Category: {cat_name} (ID: {target_cat_id})")

    print(f"Fetching posts for category '{cat_name}'...")
    all_posts = []
    page = 1
    while True:
        res = requests.get(
            f"{BASE_URL}/posts?categories={target_cat_id}&per_page=100&page={page}",
            auth=(WP_USER, WP_PASS),
            verify=False
        )
        if res.status_code != 200:
            break
        
        posts = res.json()
        if not posts:
            break
            
        all_posts.extend(posts)
        page += 1

    print(f"Total posts retrieved: {len(all_posts)}")
    if len(all_posts) < 2:
        print("Not enough posts to compare.")
        sys.exit(0)

    # Fetch GA4 Data once
    ga4_stats = {}
    try:
        ga4_stats = fetch_ga4_data_1year()
    except Exception as e:
        print(f"Warning: Failed to fetch GA4 data. Error: {e}")

    print("Cleaning HTML and preparing text...")
    documents = []
    post_info = []

    for post in all_posts:
        raw_html = post['content']['rendered']
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text).strip()
        
        documents.append(text)
        
        title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text()
        link = post['link']
        
        parsed_url = urlparse(link)
        path = parsed_url.path.rstrip('/') + '/'
        
        # Headings extraction for analysis, filtering out CTA and common fluff
        ignore_headings = ['CONTACT FOR SPECIAL PRIVILEGES', 'บทความยอดนิยม', 'สารบัญ', 'สรุป', 'บทความที่เกี่ยวข้อง', 'โปรโมชั่น', 'รีวิว']
        headings = set([h.get_text(strip=True) for h in soup.find_all(['h2', 'h3']) 
                        if len(h.get_text(strip=True)) > 3 and 
                        not any(ignore.lower() == h.get_text(strip=True).lower() or ignore.lower() in h.get_text(strip=True).lower() for ignore in ignore_headings)])
        
        # Word count
        thai_word_count = count_thai_words(text)
        
        # GA4 mapping
        stats = ga4_stats.get(path, {'activeUsers': 0, 'avgEngagementTime': 0.0, 'engagementRate': 0.0})
        
        post_info.append({
            'title': title,
            'url': link,
            'word_count': thai_word_count,
            'ga4': stats,
            'headings': headings
        })

    print("Calculating TF-IDF and Cosine Similarity...")
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 5))
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    high_sim_pairs = []
    for i in range(len(all_posts)):
        for j in range(i + 1, len(all_posts)):
            score = similarity_matrix[i][j]
            if score >= threshold:
                h1 = post_info[i]['headings']
                h2 = post_info[j]['headings']
                shared_h = h1.intersection(h2)
                
                if shared_h:
                    # Sort shared headings by length descending to show the most detailed/specific ones first
                    sorted_shared = sorted(list(shared_h), key=len, reverse=True)
                    sample = sorted_shared[:3]
                    reason = f"มีหัวข้อย่อย (H2/H3) ซ้ำกัน {len(shared_h)} หัวข้อ เช่น '{sample[0]}'"
                    if len(sample) > 1:
                        reason += f", '{sample[1]}'"
                    if len(sample) > 2:
                        reason += f", '{sample[2]}'"
                else:
                    reason = "เนื้อหา/ย่อหน้าภายในมีการใช้แพทเทิร์นหรือข้อความซ้ำกัน (ไม่มีหัวข้อที่ตรงกันเป๊ะ)"
                    
                high_sim_pairs.append({
                    'score': score,
                    'post1': post_info[i],
                    'post2': post_info[j],
                    'reason': reason
                })

    high_sim_pairs = sorted(high_sim_pairs, key=lambda x: x['score'], reverse=True)

    print(f"\n--- Duplicate / Similar Content Report (Threshold: > {threshold*100:.0f}%) ---")
    if args.output and args.output.endswith('.html'):
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Duplicate Content Report: {cat_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans Thai', sans-serif; background-color: #f8fafc; }}</style>
</head>
<body class="p-8 text-slate-800">
    <div class="max-w-6xl mx-auto">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-slate-800">รายงานบทความซ้ำซ้อน (Duplicate Content)</h1>
            <p class="text-slate-600 mt-2">หมวดหมู่: <span class="font-semibold text-blue-600">{cat_name}</span> | จำนวนคู่ที่พบ: <span class="font-semibold text-red-600">{len(high_sim_pairs)} คู่</span> | ความเหมือนขั้นต่ำ: {threshold*100:.0f}%</p>
        </header>
''')
            if not high_sim_pairs:
                f.write('<p class="text-emerald-600 font-semibold">ไม่พบบทความซ้ำซ้อนที่เกินเกณฑ์ที่กำหนด</p>')
            else:
                for idx, pair in enumerate(high_sim_pairs, 1):
                    sim_color = "text-red-600" if pair['score'] > 0.7 else "text-orange-500"
                    
                    p1 = pair['post1']
                    p2 = pair['post2']
                    reason = pair['reason']
                    
                    eng_color1 = "text-orange-500" if p1['ga4']['avgEngagementTime'] < 60 else "text-teal-600"
                    eng_color2 = "text-orange-500" if p2['ga4']['avgEngagementTime'] < 60 else "text-teal-600"
                    
                    f.write(f'''
        <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm mb-4">
            <div class="flex justify-between items-center mb-3 border-b border-slate-100 pb-2">
                <h2 class="text-lg font-bold text-slate-700">คู่ที่ {idx}</h2>
                <span class="text-xl font-bold {sim_color}">เหมือนกัน {pair['score'] * 100:.2f}%</span>
            </div>
            <div class="mb-4 p-3 bg-yellow-50 border border-yellow-100 rounded-lg">
                <p class="text-sm text-yellow-800"><span class="font-bold">สาเหตุที่เหมือนกัน:</span> {reason}</p>
            </div>
            <div class="grid grid-cols-2 gap-6">
                
                <!-- Post A -->
                <div class="bg-slate-50 border border-slate-100 p-5 rounded-lg flex flex-col justify-between">
                    <div>
                        <p class="text-xs text-slate-400 font-bold tracking-wider uppercase mb-2">Post A</p>
                        <a href="{p1['url']}" target="_blank" class="text-blue-600 hover:underline font-semibold text-lg line-clamp-2" title="{p1['title']}">{p1['title']}</a>
                    </div>
                    
                    <div class="mt-4 grid grid-cols-2 gap-4">
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">จำนวนคำไทย</p>
                            <p class="text-lg font-bold text-slate-800">{p1['word_count']:,} คำ</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">Active Users (1Y)</p>
                            <p class="text-lg font-bold text-blue-600">{p1['ga4']['activeUsers']:,}</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">Avg. Engagement</p>
                            <p class="text-lg font-bold {eng_color1}">{p1['ga4']['avgEngagementTime']:.1f}s</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">Engagement Rate</p>
                            <p class="text-lg font-bold text-emerald-600">{p1['ga4']['engagementRate']*100:.1f}%</p>
                        </div>
                    </div>
                </div>

                <!-- Post B -->
                <div class="bg-slate-50 border border-slate-100 p-5 rounded-lg flex flex-col justify-between">
                    <div>
                        <p class="text-xs text-slate-400 font-bold tracking-wider uppercase mb-2">Post B</p>
                        <a href="{p2['url']}" target="_blank" class="text-blue-600 hover:underline font-semibold text-lg line-clamp-2" title="{p2['title']}">{p2['title']}</a>
                    </div>
                    
                    <div class="mt-4 grid grid-cols-2 gap-4">
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">จำนวนคำไทย</p>
                            <p class="text-lg font-bold text-slate-800">{p2['word_count']:,} คำ</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">Active Users (1Y)</p>
                            <p class="text-lg font-bold text-blue-600">{p2['ga4']['activeUsers']:,}</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">Avg. Engagement</p>
                            <p class="text-lg font-bold {eng_color2}">{p2['ga4']['avgEngagementTime']:.1f}s</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow-sm border border-slate-100">
                            <p class="text-xs text-slate-500">Engagement Rate</p>
                            <p class="text-lg font-bold text-emerald-600">{p2['ga4']['engagementRate']*100:.1f}%</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
''')
            f.write('''
    </div>
</body>
</html>
''')
        print(f"HTML report saved to {args.output}")
    else:
        if not high_sim_pairs:
            print("No posts found with similarity above the threshold.")
        else:
            for idx, pair in enumerate(high_sim_pairs, 1):
                print(f"\n{idx}. Similarity: {pair['score'] * 100:.2f}%")
                print(f"   - Post A: {pair['post1']['title']} ({pair['post1']['url']})")
                print(f"   - Post B: {pair['post2']['title']} ({pair['post2']['url']})")

if __name__ == "__main__":
    main()
