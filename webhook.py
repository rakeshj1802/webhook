from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Instagram/Facebook Verify Token (must match what you enter in Facebook Developers Dashboard)
VERIFY_TOKEN = 'POSEBOT123'  

# Your n8n Public Webhook URL (Example from LocalTunnel or Render)
N8N_WEBHOOK_URL = 'https://myn8nbot.loca.lt/webhook-test/1a26dc91-b446-42c8-9cfe-af2d5182b813'

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def webhook():
    if request.method == 'HEAD':
        # Respond OK for HEAD requests (some services use it)
        return '', 200

    elif request.method == 'GET':
        # Instagram Webhook Verification (Initial Setup)
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('Webhook verified successfully.')
            return challenge, 200
        else:
            print('Webhook verification failed.')
            return 'Verification failed', 403

    elif request.method == 'POST':
        # Receiving Instagram Webhook Events (Messages, Comments, etc.)
        data = request.json
        print('Received Instagram Event:', data)

        # Forwarding Data to n8n Webhook
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=data)
            print(f"Forwarded to n8n, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error forwarding to n8n: {e}")

        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
