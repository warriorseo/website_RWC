from google.oauth2 import service_account
from googleapiclient.discovery import build

creds_info = {
    'type': 'service_account',
    'project_id': 'gen-lang-client-0042204106',
    'private_key_id': '800e02ba1d02083ec1711ff5f6e033618d050e84',
    'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDCPHGzqmmzNHxw\n8i12B/ILqU6iO6VWhOzSIVqiCkRVO7p6T6/FMJhqywGtMOKDk97z3tUf72nsaP5f\n244l4uow/Ta2im7YIK6YKqroM3vD8ukhLFYxDfXA3+jcRoAX3BhSLIIGDE/f4jux\nhle+/Z7M55rDK+RSBTYaRFsU5yr0ffk0tjmCYrIutRtnp0Efq67TCJveCfdCkK9R\nRPWto5+ZUOvdCTNlFwRpByNE9WO1+AvmM7ylZriXT95PvpgMf7M8mUe2onG5Kk+x\n5HluCFhQYQXrSntLLRE6x1SbX9MUE37A7D/n6Wx1hlwiQaWFi4kiiOFpD2myRU0Y\nonOVMIFrAgMBAAECggEAHHu1psWuM2fWec+hyAW5QmmFDPhXMh1TByt5+Xos9BzK\np0YJPg72wu5bJBUfmnD0SGnccg7vRwpMhy0QptCkTCPNwq4BPDNqtwjGwD9Qfncg\nJcu1JgNojuym3qp9/UG61U4OkSl8CxZHb6yGMI1LnLu377f/huGZwfdVLfcKTwjq\nt5J9Kg3vPIkKokaiehLo+4eOEupuZfjXUoV7aY/vDrAl8LlGgJg5YYRG1wLnKQ5D\nVL0jcecNA5HQ6DSdyGJ6leVJWoYAcTi4qMhOi0EABRmZM72hYIWpMHOJjedpurro\nxtndjUwr/JqVNY7Tqkv0QU7OcciJYpvHrFLhKWLDMQKBgQDkd0u/2O6hhucbaJ56\nLrUPPr/O2mTtKe9975lSoHuOJoXBvUv8C010xkbSytDVJAFUh8juMcDUOMMRfm/P\nNC4sfQNMqonvzmSYr32JGNwg5zosqrMw6YQ+dmmyYB9h/zRYn0PrwDt+Rk6lW7Fk\n2mPQvcR7XcrvEpbDX+IsdmjKWwKBgQDZpRO5TD77ZkhDAf9JlFkB8J9Ugb8ix0kb\nqYsxtR+iWnRqfzqbO0tu2hK8FceIuW3lR09aATMxbbKt5A9Y+wv9aJq6k3+HcDw9\n42/XIcmp4gQyz92LPWQ2dHyxY8gW/VVux0XJJ/CYuVFslhveBsj7hsuEdjDoxB4W\npRCGFZQyMQKBgGmRgkwc5m93EZVFq20T5hAsU582pUo9hW+w5i0bANy3ijjyyoil\nhF4APLusggDrCT5RHBSMouitbd3Iicu59dgS0BJ9/wzzVuKCvMQ724PMtMHtAq4I\nSVY/iymkZvv2W+7TcSQfiJ4ZyL959id/Dn5nIcJLnbkI4udWiAE5mcRfAoGAcaEl\n8xBDsa1s/M8GIbw53DFsfgpfaCDzomWaLpGJupHPReq3BmSmtXFVZq1YR6HIJnRc\nkXke6SeEqhTvjl1DnUIHxnFLm8KVMRqVQZR6XR+LYZv05sVelK+silC2HoqVGAkh\n/ivECXh3cmHMmtagB/IQP1AVqPD7ZIc5YUfS34ECgYB0pT6N5TbPDKHfftsZNgI0\nHHQN07jruHQ5naDR5L7F2n4rSVJH7dcwedHZaQxR+F1fYdKEWstqR73WPW4chluR\nyNE53+Xlt+Yt3cRhTKNBtCV7EMiA0S/yIt0Ai20o5MOc3P1xys1AopxFKFE1xBNm\nvQV+INvYA9APPlVNSKshbQ==\n-----END PRIVATE KEY-----\n',
    'client_email': 'aiwar-841@gen-lang-client-0042204106.iam.gserviceaccount.com',
    'token_uri': 'https://oauth2.googleapis.com/token',
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'
SHEET_NAME = 'Improve Engagement'

content = [
    "⭐ [H1] โปรแกรมฉีด ฟิลเลอร์สะโพก คู่มือต้องรู้ก่อนฉีดโดยหมอขนม",
    "  🔹 [H2] สารบัญฟิลเลอร์สะโพก",
    "  🔹 [H2] ฟิลเลอร์สะโพก คืออะไร",
    "  🔹 [H2] ฟิลเลอร์สะโพก ดีอย่างไร",
    "  🔹 [H2] ฟิลเลอร์สะโพก เหมาะกับใครบ้าง",
    "  🔹 [H2] ทรงสะโพกยอดนิยม",
    "  🔹 [H2] การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก",
    "      🔸 [H3] ข้อควรปฏิบัติก่อนฉีด",
    "      🔸 [H3] ข้อควรปฏิบัติหลังฉีด",
    "  🔹 [H2] อาการข้างเคียงที่อาจเกิดขึ้นหลังฉีด",
    "  🔹 [H2] ฟิลเลอร์สะโพก Variofill",
    "  🔹 [H2] ผลลัพธ์อยู่ได้นานแค่ไหน",
    "  🔹 [H2] ฟิลเลอร์สะโพก ราคาเท่าไหร่",
    "  🔹 [H2] เทคนิคการฉีดฟิลเลอร์สะโพก",
    "  🔹 [H2] ขั้นตอนการฉีดฟิลเลอร์สะโพก",
    "      🔸 [H3] ขั้นตอนที่ 1 (ถึง ขั้นตอนที่ 7)",
    "  🔹 [H2] ฉีดฟิลเลอร์สะโพกชั้นไหน?",
    "  🔹 [H2] ฉีดฟิลเลอร์สะโพกด้วย Variofill",
    "  🔹 [H2] ฟิลเลอร์สะโพก VS ศัลยกรรมสะโพก VS ฉีดไขมันสะโพก",
    "      🔸 [H3] การศัลยกรรมสะโพก",
    "      🔸 [H3] ฉีดไขมันสะโพก",
    "  🔹 [H2] ฉีดฟิลเลอร์สะโพกกับหมอขนมดีอย่างไร",
    "  🔹 [H2] Q&A",
    "      🔸 [H3] 1. การฉีดฟิลเลอร์สะโพกอยู่ได้ถาวรหรือไม่",
    "      🔸 [H3] 2. จะดูแข็งเป็นก้อนหรือไม่",
    "      🔸 [H3] 3. มีรอยแผลเป็นหรือไม่",
    "      🔸 [H3] 4. ฉีดสะโพกด้วยฟิลเลอร์ยี่ห้ออื่นได้ไหม?",
    "  🔹 [H2] รีวิวการฉีดฟิลเลอร์สะโพก",
    "  🔹 [H2] บทสรุป"
]

values = [[item] for item in content]

body = {
    'values': values
}

# Update values starting at A2
range_name = f"{SHEET_NAME}!A2:A{len(values) + 1}"
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_name,
    valueInputOption='USER_ENTERED', body=body).execute()

print(f"{result.get('updatedCells')} cells updated.")
