import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

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
        
    # Match pattern: A:100 | T:30s | E:34%
    # Regex: A:(\d+) \| T:(\d+)s \| E:(\d+)%
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

def main():
    sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    target_sheet_name = None
    for s in sheets:
        if s.get("properties", {}).get("sheetId") == target_gid:
            target_sheet_name = s.get("properties", {}).get("title")
            break

    print("Fetching data...")
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A1:L").execute()
    rows = result.get('values', [])
    
    candidates = []
    
    for i, row in enumerate(rows):
        if i == 0 or len(row) < 12:
            continue
            
        url = row[0]
        col_l_val = row[11] # Combined Summary
        
        parsed = parse_combined_cell(col_l_val)
        if parsed:
            # We want pages that:
            # 1. Had good engagement time last year (e.g. past_time >= 40s)
            # 2. Had good engagement rate last year (e.g. past_eng >= 50%)
            # 3. Drop in time_pct <= -20% OR drop in eng_pct <= -15% OR user_pct <= -20%
            if parsed["past_time"] >= 45 and parsed["past_eng"] >= 50:
                if parsed["time_pct"] <= -20 or parsed["eng_pct"] <= -15 or parsed["user_pct"] <= -20:
                    candidates.append({
                        "url": url,
                        "metrics": parsed
                    })

    print(f"Found {len(candidates)} candidates.")
    # Sort candidates by time drop
    candidates.sort(key=lambda x: x["metrics"]["time_pct"])
    
    for c in candidates[:15]:
        m = c["metrics"]
        print(f"\nURL: {c['url']}")
        print(f"  Users: {m['curr_users']} vs {m['past_users']} ({m['user_pct']:+.0f}%)")
        print(f"  Time: {m['curr_time']:.0f}s vs {m['past_time']:.0f}s ({m['time_pct']:+.0f}%)")
        print(f"  Eng Rate: {m['curr_eng']:.0f}% vs {m['past_eng']:.0f}% ({m['eng_pct']:+.0f}%)")

if __name__ == "__main__":
    main()
