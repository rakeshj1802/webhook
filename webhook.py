from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Instagram/Facebook Verify Token (must match what you enter in Facebook Developers Dashboard)
VERIFY_TOKEN = 'POSEBOT123'  

# Your n8n Public Webhook URL (Example from LocalTunnel or Render)
N8N_WEBHOOK_URL = 'https://myn8nbot.loca.lt/webhook-test/1a26dc91-b446-42c8-9cfe-af2d5182b813'

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def webhook_or_oauth():
    if request.method == 'HEAD':
        return '', 200

    elif request.method == 'GET':
        if 'hub.mode' in request.args:
            # Handle Webhook Verification
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
            # Handle OAuth Redirect
            code = request.args.get('code')
            print(f"Received OAuth Code: {code}")
            return f'OAuth code received: {code}', 200
        else:
            return 'Unknown GET request.', 400

    elif request.method == 'POST':
        data = request.json
        print('Received Instagram Webhook Event:', data)

        # Forward to n8n (as before)
        try:
            requests.post(N8N_WEBHOOK_URL, json=data)
        except Exception as e:
            print(f"Error forwarding to n8n: {e}")

        return 'EVENT_RECEIVED', 200
