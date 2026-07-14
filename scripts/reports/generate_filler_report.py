import os
import re
import datetime
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
import urllib.parse

load_dotenv(r"d:\AI-Cyborg-2558\00_agents\.env")

private_key = os.environ.get("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")
credentials_info = {
    "type": os.environ.get("GOOGLE_SERVICE_ACCOUNT_TYPE"),
    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

sheet_id = "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ"
target_gid = 199841076

def parse_combined_cell(cell_val):
    if not cell_val or cell_val == "N/A" or "A:" not in cell_val:
        return None
        
    lines = cell_val.strip().split('\n')
    if len(lines) < 3:
        return None
        
    pattern = r"A:([-\d\+]+)%? \| T:([-\d\+]+)s?%? \| E:([-\d\+]+)%?"
    
    m1 = re.match(pattern, lines[0])
    m2 = re.match(pattern, lines[1])
    m3 = re.match(pattern, lines[2])
    
    if not m1 or not m2 or not m3:
        return None
        
    curr_users = int(m1.group(1))
    curr_time = float(m1.group(2))
    curr_eng = float(m1.group(3))
    
    past_users = int(m2.group(1))
    past_time = float(m2.group(2))
    past_eng = float(m2.group(3))
    
    user_pct = float(m3.group(1))
    time_pct = float(m3.group(2))
    eng_pct = float(m3.group(3))
    
    return {
        "curr_users": curr_users,
        "curr_time": curr_time,
        "curr_eng": curr_eng,
        "past_users": past_users,
        "past_time": past_time,
        "past_eng": past_eng,
        "user_pct": user_pct,
        "time_pct": time_pct,
        "eng_pct": eng_pct
    }

def fetch_filler_urls():
    cat_id = 112
    urls = []
    page = 1
    while True:
        res = requests.get(f"https://rwcclinic.com/wp-json/wp/v2/posts?categories={cat_id}&per_page=100&page={page}")
        if res.status_code != 200:
            break
        posts = res.json()
        if not posts:
            break
        for p in posts:
            link = p['link'].lower().rstrip('/')
            link = urllib.parse.unquote(link)
            urls.append(p['link'])
        page += 1
    return urls

def main():
    print("Fetching Filler URLs from WP API (Category 112)...")
    filler_urls_raw = fetch_filler_urls()
    print(f"Found {len(filler_urls_raw)} articles.")
    
    sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    target_sheet_name = None
    for s in sheets:
        if s.get("properties", {}).get("sheetId") == target_gid:
            target_sheet_name = s.get("properties", {}).get("title")
            break

    print("Fetching data from Sheet...")
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A1:M").execute()
    rows = result.get('values', [])
    
    sheet_data = {}
    type_counts = {"Article": 0, "News": 0, "Page": 0, "Service": 0}
    
    for i, row in enumerate(rows):
        if i == 0 or len(row) < 2:
            continue
        url_raw = row[0]
        url_key = urllib.parse.unquote(url_raw.lower().rstrip('/'))
        
        t = row[1]
        type_counts[t] = type_counts.get(t, 0) + 1
        
        if len(row) < 13:
            continue
            
        col_l_val = row[11]
        ga4_link_compare = row[12]
        
        link_match = re.search(r'=HYPERLINK\("([^"]+)"', ga4_link_compare)
        ga4_url = link_match.group(1) if link_match else "#"
        
        parsed = parse_combined_cell(col_l_val)
        sheet_data[url_key] = {
            "metrics": parsed,
            "ga4_url": ga4_url,
            "type": t
        }
        
    neg_candidates = []
    pos_candidates = []
    
    for url in filler_urls_raw:
        url_key = urllib.parse.unquote(url.lower().rstrip('/'))
        if url_key in sheet_data:
            data = sheet_data[url_key]
            m = data["metrics"]
            if m:
                # Both Engagement Time AND Engagement Rate dropped
                if m["time_pct"] < 0 and m["eng_pct"] < 0:
                    neg_candidates.append({
                        "url": url,
                        "ga4_url": data["ga4_url"],
                        "metrics": m,
                        "type": data["type"]
                    })
                # Both Engagement Time AND Engagement Rate improved
                elif m["time_pct"] > 0 and m["eng_pct"] > 0:
                    pos_candidates.append({
                        "url": url,
                        "ga4_url": data["ga4_url"],
                        "metrics": m,
                        "type": data["type"]
                    })
            
    # Sort neg drops by time drop percent (lowest/most negative first)
    neg_candidates.sort(key=lambda c: c["metrics"]["time_pct"])
    # Sort pos gains by time drop percent (highest/most positive first)
    pos_candidates.sort(key=lambda c: c["metrics"]["time_pct"], reverse=True)
    
    today = datetime.datetime.now()
    
    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>รายงานการวิเคราะห์กู้ทราฟฟิกหมวดหมู่ Filler - RWC Clinic</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Noto+Sans+Thai:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {{
            font-family: 'Outfit', 'Noto Sans Thai', sans-serif;
            background-color: #f8fafc;
        }}
    </style>
</head>
<body class="p-8 text-slate-800">
    <div class="max-w-7xl mx-auto">
        <header class="flex justify-between items-center mb-12 pb-6 border-b border-slate-200">
            <div>
                <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-700 to-purple-700 bg-clip-text text-transparent">รายงานการวิเคราะห์กู้ทราฟฟิกหมวดหมู่ Filler</h1>
                <p class="text-slate-600 text-lg mt-2">วิเคราะห์ข้อมูลเปรียบเทียบ YTD (ปี 2026 เทียบกับ 2025 ช่วงเวลาเดียวกันสะสม)</p>
            </div>
            <div class="text-right">
                <p class="font-semibold text-slate-800">ลูกค้า: RWC Clinic</p>
                <p class="text-sm text-slate-500">วันที่รายงาน: {today.strftime('%d/%m/%Y')}</p>
            </div>
        </header>

        <div class="grid grid-cols-1 mb-12">
            <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:-translate-y-1 transition-transform duration-200">
                <div class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-4">สัดส่วนประเภทหน้าเว็บทั้งหมดในชีต (Total Pages Breakdown)</div>
                <div class="flex flex-wrap justify-around items-center text-lg font-semibold py-2">
                    <span class="flex items-center text-blue-600"><i data-lucide="file-text" class="w-5 h-5 mr-2"></i> บทความ (Article): {type_counts.get('Article', 0)} หน้า</span>
                    <span class="flex items-center text-amber-600"><i data-lucide="newspaper" class="w-5 h-5 mr-2"></i> ข่าวสาร (News): {type_counts.get('News', 0)} หน้า</span>
                    <span class="flex items-center text-purple-500"><i data-lucide="sparkles" class="w-5 h-5 mr-2"></i> บริการ (Service): {type_counts.get('Service', 0)} หน้า</span>
                    <span class="flex items-center text-emerald-600"><i data-lucide="layout-template" class="w-5 h-5 mr-2"></i> หน้าหลัก/อื่นๆ (Page): {type_counts.get('Page', 0)} หน้า</span>
                </div>
                <div class="text-sm text-slate-500 mt-2 text-center">วิเคราะห์จากข้อมูลโครงสร้างตารางคัดกรองทั้งหมด 687 บรรทัด (ไม่รวมหัวตาราง)</div>
            </div>
        </div>

        <!-- Section 1: Negative Drops -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 gap-4">
            <div>
                <h2 class="text-2xl font-bold text-slate-800">บทความที่ประสิทธิภาพลดลง (Negative Drops)</h2>
                <p class="text-slate-500 mt-1">คัดกรองเฉพาะหน้าที่ <span class="font-semibold text-red-600">Engagement Time</span> และ <span class="font-semibold text-red-600">Engagement Rate</span> ลดลงทั้งคู่</p>
                <p class="text-slate-500 mt-1">พบทั้งหมด <span class="font-bold text-red-600 text-lg">{len(neg_candidates)} บทความ</span> จากบทความหมวดหมู่ Filler ทั้งหมด {len(filler_urls_raw)} บทความ</p>
            </div>
            <input type="text" id="searchInput" class="bg-white border border-slate-200 rounded-lg px-4 py-2 text-slate-800 w-full max-w-md outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" placeholder="ค้นหา URL หน้าเว็บ (ค้นหาได้ทั้ง 2 ตาราง)...">
        </div>

        <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm mb-12">
            <table class="w-full text-left border-collapse report-table">
                <thead>
                    <tr class="bg-slate-50 border-b border-slate-200">
                        <th class="py-4 px-6 font-semibold text-slate-600 w-16 text-center">#</th>
                        <th class="py-4 px-6 font-semibold text-slate-600">URL หน้าเว็บ</th>
                        <th class="py-4 px-6 font-semibold text-slate-600">Active Users (YoY)</th>
                        <th class="py-4 px-6 font-semibold text-slate-600">Avg. Engagement Time (YoY)</th>
                        <th class="py-4 px-6 font-semibold text-slate-600">Avg. Engagement Rate (YoY)</th>
                        <th class="py-4 px-6 font-semibold text-slate-600">ลิงก์ GA4</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-200">
    """
        
    def build_row(c, index):
        url_short = urllib.parse.unquote(c["url"]).replace("https://rwcclinic.com", "")
        m = c["metrics"]
        
        u_class = "text-red-600" if m["user_pct"] < 0 else "text-emerald-600"
        t_class = "text-red-600" if m["time_pct"] < 0 else "text-emerald-600"
        e_class = "text-red-600" if m["eng_pct"] < 0 else "text-emerald-600"
        
        users_html = f"{int(m['curr_users'])} | {int(m['past_users'])}<span class='block font-semibold mt-1 {u_class}'>{m['user_pct']:+.0f}%</span>"
        time_html = f"{m['curr_time']:.1f}s | {m['past_time']:.1f}s<span class='block font-semibold mt-1 {t_class}'>{m['time_pct']:+.0f}%</span>"
        eng_html = f"{m['curr_eng']:.0f}% | {m['past_eng']:.0f}%<span class='block font-semibold mt-1 {e_class}'>{m['eng_pct']:+.0f}%</span>"
        
        ga4_btn = f'<a href="{c["ga4_url"]}" target="_blank" class="bg-blue-50 text-blue-600 border border-blue-200 px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-blue-600 hover:text-white transition-colors whitespace-nowrap">เปิด GA4</a>' if c["ga4_url"] != "#" else ""
        
        return f"""
                    <tr class="hover:bg-slate-50/50 transition-colors search-row">
                        <td class="py-4 px-6 text-center text-slate-400 font-semibold">{index + 1}</td>
                        <td class="py-4 px-6">
                            <a href="{c['url']}" target="_blank" class="text-blue-600 font-semibold hover:underline block max-w-sm truncate" title="{urllib.parse.unquote(c['url'])}">{url_short}</a>
                        </td>
                        <td class="py-4 px-6 text-sm">{users_html}</td>
                        <td class="py-4 px-6 text-sm">{time_html}</td>
                        <td class="py-4 px-6 text-sm">{eng_html}</td>
                        <td class="py-4 px-6">{ga4_btn}</td>
                    </tr>"""

    for index, c in enumerate(neg_candidates):
        html_content += build_row(c, index)

    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <!-- Section 2: Positive Gains -->
        <div class="flex justify-between items-end mb-6 mt-16">
            <div>
                <h2 class="text-2xl font-bold text-slate-800">บทความที่ประสิทธิภาพดีขึ้น (Performance Improved)</h2>
                <p class="text-slate-500 mt-1">คัดกรองเฉพาะหน้าที่ <span class="font-semibold text-emerald-600">Engagement Time</span> และ <span class="font-semibold text-emerald-600">Engagement Rate</span> เพิ่มขึ้นทั้งคู่</p>
                <p class="text-slate-500 mt-1">พบทั้งหมด <span class="font-bold text-emerald-600 text-lg">{len(pos_candidates)} บทความ</span> จากบทความหมวดหมู่ Filler ทั้งหมด {len(filler_urls_raw)} บทความ</p>
            </div>
        </div>

    </div>

    <script>
        lucide.createIcons();
        document.getElementById('searchInput').addEventListener('keyup', function() {{
            var input = this.value.toLowerCase();
            var rows = document.querySelectorAll('.report-table tbody .search-row');
            for (var i = 0; i < rows.length; i++) {{
                var urlText = rows[i].querySelector('td:nth-child(2)').textContent.toLowerCase();
                if (urlText.includes(input)) {{
                    rows[i].style.display = "";
                }} else {{
                    rows[i].style.display = "none";
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    report_path = "d:\\AI-Cyborg-2558\\_SEO_Clients\\RWC\\web\\filler_traffic_recovery_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Report generated successfully at: {report_path}")

if __name__ == "__main__":
    main()
