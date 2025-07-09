from flask import Flask, request
import requests  # For forwarding messages to n8n

app = Flask(__name__)

VERIFY_TOKEN = 'POSEBOT123'  # Must exactly match Facebook Developer Verify Token

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def webhook():
    if request.method == 'HEAD':
        return '', 200

    elif request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('Webhook verified successfully.')
            return challenge, 200
        else:
            print('Verification failed.')
            return 'Verification failed', 403

    elif request.method == 'POST':
        data = request.json
        print('Received Instagram Message:', data)

        # Your n8n webhook URL (replace with your real URL)
        n8n_webhook_url = 'http://localhost:5678/webhook-test/instagram_chat'

        try:
            response = requests.post(n8n_webhook_url, json=data)
            print(f"Forwarded to n8n, status code: {response.status_code}")
        except Exception as e:
            print(f"Error forwarding to n8n: {e}")

        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
