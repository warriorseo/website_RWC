import os
import sys
import requests
import urllib3
import re
import argparse
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from bs4 import MarkupResemblesLocatorWarning
from pythainlp.tokenize import word_tokenize
import numpy as np

def thai_tokenizer(text):
    return word_tokenize(text, engine='newmm')

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    Filter,
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
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="sessionDefaultChannelGroup",
                in_list_filter=Filter.InListFilter(
                    values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"]
                )
            )
        ),
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
        
        # Build complex GA4 URL
        ga4_path = quote(path, safe='')
        ga4_path_double = quote(ga4_path, safe='')
        ga4_deep_link = (
            "https://analytics.google.com/analytics/web/#/a149800124p292925407/reports/explorer?"
            "params=_u..nav%3Dmaui%26_u..built_comparisons_enabled%3Dtrue%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%227523527606%22,%22name%22:%22Organic%20traffic%22,%22isEnabled%22:true,%22filters%22:%5B%7B%22fieldName%22:%22sessionDefaultChannelGrouping%22,%22evaluationType%22:8,%22expressionList%22:%5B%22Organic%20Search%22,%22Organic%20Video%22,%22Organic%20Social%22,%22Organic%20Shopping%22%5D,%22isCaseSensitive%22:true%7D%5D,%22systemDefinedSavedComparisonType%22:2,%22isSystemDefined%22:true%7D%5D%26_u.dateOption%3DyearToDate%26_u.comparisonOption%3Ddisabled%26_r.explorerCard..filterTerm%3D"
            + ga4_path_double +
            "%26_r.explorerCard..startRow%3D0&r=all-pages-and-screens"
        )
        
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
            'ga4_deep_link': ga4_deep_link,
            'word_count': thai_word_count,
            'ga4': stats,
            'headings': headings,
            'clean_text': text
        })

    print("Calculating TF-IDF and Cosine Similarity...")
    vectorizer = TfidfVectorizer(tokenizer=thai_tokenizer, min_df=2, max_df=0.95)
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
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
                
                vec_a = tfidf_matrix[i].toarray()[0]
                vec_b = tfidf_matrix[j].toarray()[0]
                shared_indices = np.where((vec_a > 0) & (vec_b > 0))[0]
                shared_words = []
                for si in shared_indices:
                    shared_words.append({'word': feature_names[si], 'weight': vec_a[si] * vec_b[si]})
                shared_words = sorted(shared_words, key=lambda x: x['weight'], reverse=True)
                top_shared = shared_words[:20]
                
                # Unique A
                unique_a_indices = np.where((vec_a > 0) & (vec_b == 0))[0]
                unique_a_words = [{'word': feature_names[si], 'weight': vec_a[si]} for si in unique_a_indices]
                top_unique_a = sorted(unique_a_words, key=lambda x: x['weight'], reverse=True)[:15]
                
                # Unique B
                unique_b_indices = np.where((vec_b > 0) & (vec_a == 0))[0]
                unique_b_words = [{'word': feature_names[si], 'weight': vec_b[si]} for si in unique_b_indices]
                top_unique_b = sorted(unique_b_words, key=lambda x: x['weight'], reverse=True)[:15]
                
                # Exact phrases
                ignore_exact_phrases = [
                    "กดด้านล่างติดเราเพื่อสอบถามรายละเอียด",
                    "กดด้านล่างติดเรา",
                    "สอบถามรายละเอียดเเละสิทธิ์อื่นๆ",
                    "ทีมแพทย์ผู้เชี่ยวชาญด้านผิวหนัง",
                    "สงวนลิขสิทธิ์",
                    "อ่านเพิ่มเติม",
                    "บทความที่เกี่ยวข้อง",
                    "ติดต่อเรา"
                ]
                clauses_a = [c.strip() for c in re.split(r'[\n\s]+', post_info[i]['clean_text']) if len(c.strip()) > 30 and not any(ign in c for ign in ignore_exact_phrases)]
                clauses_b = [c.strip() for c in re.split(r'[\n\s]+', post_info[j]['clean_text']) if len(c.strip()) > 30 and not any(ign in c for ign in ignore_exact_phrases)]
                shared_clauses = list(set(clauses_a).intersection(set(clauses_b)))
                top_shared_clauses = shared_clauses[:5]
                    
                high_sim_pairs.append({
                    'score': score,
                    'post1': post_info[i],
                    'post2': post_info[j],
                    'reason': reason,
                    'top_shared': top_shared,
                    'total_shared': len(shared_indices),
                    'top_unique_a': top_unique_a,
                    'top_unique_b': top_unique_b,
                    'top_shared_clauses': top_shared_clauses,
                    'shared_h': list(shared_h) if shared_h else []
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

        <details class="bg-white border border-slate-200 rounded-lg shadow-sm mb-8 group">
            <summary class="cursor-pointer p-4 font-semibold text-slate-700 bg-slate-50 rounded-t-lg hover:bg-slate-100 flex justify-between items-center outline-none">
                <span>⚙️ ระบบนี้วิเคราะห์ความซ้ำซ้อนอย่างไร? (TF-IDF & Cosine Similarity)</span>
                <span class="text-slate-400 group-open:rotate-180 transition-transform duration-200">▼</span>
            </summary>
            <div class="p-6 border-t border-slate-200 text-sm text-slate-600 leading-relaxed bg-white">
                <p class="mb-3"><strong>1. การตัดคำ (Tokenization):</strong> ระบบใช้เทคโนโลยี AI (PyThaiNLP) ในการอ่านเนื้อหาทั้งหมดและตัดประโยคภาษาไทยที่เขียนติดกันยาวๆ ออกเป็น "คำย่อยๆ" ได้อย่างแม่นยำ (เช่น "ฉีด", "ฟิลเลอร์", "หน้า")</p>
                <p class="mb-3"><strong>2. การให้น้ำหนักคำ (TF-IDF):</strong> 
                   <br><span class="ml-4">- <strong>TF (Term Frequency):</strong> นับว่าคำศัพท์แต่ละคำปรากฏบ่อยแค่ไหนใน 1 บทความ</span>
                   <br><span class="ml-4">- <strong>IDF (Inverse Document Frequency):</strong> ระบบจะลดความสำคัญของ "คำที่เจอได้ทั่วไปในทุกหน้า" (เช่น คือ, และ, ทำให้) และเพิ่มความสำคัญให้ "คำเฉพาะเจาะจง" ที่โผล่มาแค่บางบทความ</span></p>
                <p><strong>3. การเทียบความเหมือน (Cosine Similarity):</strong> นำสัดส่วนคำศัพท์ทั้งหมดของ 2 บทความมาแปลงเป็นเวกเตอร์ทางคณิตศาสตร์ และเทียบมุมองศากันเพื่อให้ได้เปอร์เซ็นต์ความเหมือน (0-100%) ที่แม่นยำที่สุด ไม่ใช่แค่การนับคำซ้ำทื่อๆ</p>
            </div>
        </details>
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
                        <a href="{p1['ga4_deep_link']}" target="_blank" class="text-xs text-orange-600 hover:underline mt-1 inline-block" title="คลิกเพื่อดูสถิติหน้านี้แบบ Organic Traffic ย้อนหลัง 1 ปี ใน GA4">📊 เช็คข้อมูลเจาะลึกหน้านี้ใน GA4</a>
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
                        <a href="{p2['ga4_deep_link']}" target="_blank" class="text-xs text-orange-600 hover:underline mt-1 inline-block" title="คลิกเพื่อดูสถิติหน้านี้แบบ Organic Traffic ย้อนหลัง 1 ปี ใน GA4">📊 เช็คข้อมูลเจาะลึกหน้านี้ใน GA4</a>
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
            
            <details class="mt-4 border border-slate-200 rounded-lg group">
                <summary class="cursor-pointer p-3 text-sm font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 flex justify-between items-center rounded-lg outline-none group-open:rounded-b-none group-open:border-b border-slate-200">
                    <span>🔍 ดูข้อมูลวิเคราะห์เชิงลึก (Deep Analysis)</span>
                    <span class="text-slate-400 group-open:rotate-180 transition-transform duration-200">▼</span>
                </summary>
                <div class="p-5 bg-white text-sm text-slate-600 rounded-b-lg space-y-6">
                    
                    <!-- Exact Matches -->
                    <div>
                        <h4 class="font-bold text-slate-800 mb-2 border-l-4 border-red-500 pl-2">🚨 หลักฐานการก็อปปี้ประโยค (Exact Phrase Matches)</h4>
                        {f'<ul class="list-disc pl-5 space-y-1 text-red-600">{"".join([f"<li>{c}</li>" for c in pair["top_shared_clauses"]])}</ul>' if pair['top_shared_clauses'] else '<p class="text-slate-500">ไม่พบประโยคยาวๆ ที่เหมือนกันเป๊ะ 100%</p>'}
                    </div>

                    <!-- Shared Headings -->
                    <div>
                        <h4 class="font-bold text-slate-800 mb-2 border-l-4 border-orange-400 pl-2">📑 โครงสร้างหัวข้อที่ซ้ำกัน (Shared Headings)</h4>
                        {f'<ul class="list-disc pl-5 space-y-1 text-orange-600">{"".join([f"<li>{h}</li>" for h in pair["shared_h"]])}</ul>' if pair['shared_h'] else '<p class="text-slate-500">ไม่พบหัวข้อย่อยที่ตั้งชื่อเหมือนกันเป๊ะ 100%</p>'}
                    </div>
                    
                    <!-- Unique A -->
                    <div>
                        <h4 class="font-bold text-slate-800 mb-2 border-l-4 border-emerald-500 pl-2">✨ คำศัพท์เฉพาะของ Post A (พบ {len(pair["top_unique_a"])} คำที่น้ำหนักสูงสุด)</h4>
                        <div class="flex flex-wrap gap-2">
                            {"".join([f'<span class="px-2 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md shadow-sm" title="Weight: {w["weight"]:.4f}">{w["word"]}</span>' for w in pair['top_unique_a'] if w['word'].strip()])}
                        </div>
                    </div>

                    <!-- Unique B -->
                    <div>
                        <h4 class="font-bold text-slate-800 mb-2 border-l-4 border-emerald-500 pl-2">✨ คำศัพท์เฉพาะของ Post B (พบ {len(pair["top_unique_b"])} คำที่น้ำหนักสูงสุด)</h4>
                        <div class="flex flex-wrap gap-2">
                            {"".join([f'<span class="px-2 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md shadow-sm" title="Weight: {w["weight"]:.4f}">{w["word"]}</span>' for w in pair['top_unique_b'] if w['word'].strip()])}
                        </div>
                    </div>

                    <!-- Shared Terms -->
                    <div>
                        <h4 class="font-bold text-slate-800 mb-2 border-l-4 border-blue-500 pl-2">🔄 คำศัพท์แกนหลักที่ซ้ำซ้อนกัน (Shared Terms: {pair['total_shared']} คำ)</h4>
                        <div class="flex flex-wrap gap-2">
                            {"".join([f'<span class="px-2 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded-md shadow-sm" title="Weight: {w["weight"]:.4f}">{w["word"]}</span>' for w in pair['top_shared'] if w['word'].strip()])}
                        </div>
                    </div>

                </div>
            </details>
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
