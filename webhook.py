# webhook.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "POSEBOT123")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403

    elif request.method == 'POST':
        # Handle incoming WhatsApp messages
        data = request.get_json()
        print("Received webhook data:", data)
        return "EVENT_RECEIVED", 200

    return "Not allowed", 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
