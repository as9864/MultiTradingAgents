# auto/slack_notifier.py

import requests
import os

# 슬랙 Webhook URL을 환경변수 또는 직접 정의 (보안상 .env 사용 권장)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL") or "https://hooks.slack.com/services/your/webhook/url"

def send_slack_message(message: str):
    if "your/webhook/url" in SLACK_WEBHOOK_URL:
        print("⚠️ Slack Webhook URL이 설정되어 있지 않습니다.")
        return

    payload = {
        "text": message
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print(f"❌ Slack 전송 실패: {response.text}")
        else:
            print("✅ Slack 메시지 전송 완료")
    except Exception as e:
        print(f"❌ Slack 전송 에러: {e}")