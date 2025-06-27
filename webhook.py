from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "POSEBOT123")

@app.route('/')
def home():
    return "✅ WhatsApp Webhook is live."

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification handshake
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully.")
            return challenge, 200
        else:
            print("❌ Webhook verification failed.")
            return "Verification failed", 403

    if request.method == 'POST':
        data = request.get_json()
        print("📩 Received webhook event:")
        print(data)
        return "EVENT_RECEIVED", 200

    return "Method Not Allowed", 405
