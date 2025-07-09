from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = 'POSEBOT123'  
N8N_WEBHOOK_URL = 'https://myn8nbot.loca.lt/webhook-test/1a26dc91-b446-42c8-9cfe-af2d5182b813'

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def webhook_or_oauth():
    if request.method == 'HEAD':
        return '', 200

    elif request.method == 'GET':
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('Webhook verified successfully.')
                return challenge, 200
            else:
                print('Webhook verification failed.')
                return 'Verification failed', 403
        elif 'code' in request.args:
            code = request.args.get('code')
            print(f"Received OAuth Code: {code}")
            return f'OAuth code received: {code}', 200
        else:
            return 'Unknown GET request.', 400

    elif request.method == 'POST':
        data = request.json
        print('Received Instagram Webhook Event:', data)

        try:
            requests.post(N8N_WEBHOOK_URL, json=data)
            print('Forwarded to n8n successfully.')
        except Exception as e:
            print(f"Error forwarding to n8n: {e}")

        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
