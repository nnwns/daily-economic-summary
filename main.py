import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import openai

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    message = service.users().messages().send(userId=user_id, body=message).execute()
    print(f'Message Id: {message["id"]}')
    return message

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def generate_economic_summary():
    prompt = """
    전 세계 주요 경제 이슈 3~5가지를 초보자도 이해할 수 있게 중학생 수준으로 설명하고, 
    각 이슈가 주식, 채권, 암호화폐 시장에 미치는 영향과 
    오늘 시장에 미칠 종합적 영향 방향을 알려주세요. 핵심 키워드도 1~2개 제시해 주세요.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.7,
    )
    return response.choices[0].message['content']

def main():
    service = get_gmail_service()
    sender = '본인 Gmail 주소@gmail.com'
    to = sender
    subject = '[경제 요약] 전날 주요 이슈와 시장 전망'
    summary = generate_economic_summary()
    message = create_message(sender, to, subject, summary)
    send_message(service, 'me', message)

if __name__ == '__main__':
    main()