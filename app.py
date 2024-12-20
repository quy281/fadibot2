
from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

# Cập nhật dữ liệu
PAGE_ACCESS_TOKEN = "EAAIUQMreC0EBOZBOaOQIASVIAxHWhKZBe9APtMnDOV58wUUdzjZCWHLTUGwm1ZAwlqbdEMOvKEZCFiOFbQazrACZAQAxEmDbf9ZBx0dYjN5qqS3NuA7qmhRHd6FnbCg5bZCnbi9UukV3DZC1fjS0J9Sxo7MmUCSbvLbZC5Cskf4El6XrOdJUWvZAKDZCaPUPl6G2NFHpQnpB3Aji4mY9A74ZD"
VERIFY_TOKEN = "mkg20144"
OPENAI_API_KEY = "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"

# Đặt API Key cho OpenAI
openai.api_key = OPENAI_API_KEY

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        if verify_token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Invalid verification token', 403
    
    elif request.method == 'POST':
        data = request.json
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        response_text = get_chatgpt_response(message_text)
                        send_message(sender_id, response_text)
        return 'EVENT_RECEIVED', 200

def get_chatgpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Xin lỗi, tôi không thể xử lý yêu cầu của bạn ngay bây giờ."

def send_message(recipient_id, text):
    url = f'https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
