# main.py

import os
import json
import base64
import smtplib
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API 접근에 필요한 범위
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_login():
    creds = None

    # GitHub Secret에서 credentials.json 내용 읽기
    credentials_raw = os.getenv("GMAIL_CREDENTIALS")
    credentials_dict = json.loads(credentials_raw)

    # 파일로 저장
    with open('credentials.json', 'w') as f:
        json.dump(credentials_dict, f)

    # 인증 플로우 실행
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Gmail 서비스 객체 생성
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_test_email(service):
    message = MIMEText('✅ GPT 자동 메일 테스트입니다. 잘 도착했다면 설정이 성공한 것입니다!')
    message['to'] = '<wnsdud000601@icloud.com>'  # ← 본인 이메일로 변경
    message['from'] = 'me'
    message['subject'] = '테스트 메일: GPT 자동화'

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw_message}

    message = service.users().messages().send(userId='me', body=body).execute()
    print('✅ 메일 전송 성공! Message ID:', message['id'])

if __name__ == '__main__':
    gmail_service = gmail_login()
    send_test_email(gmail_service)
