from flask import Flask, request
import os

app = Flask(__name__)
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'POSTBOT123')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("✅ Webhook verified")
            return challenge, 200
        else:
            print("❌ Verification failed")
            return "Forbidden", 403

    if request.method == 'POST':
        print("📩 Webhook event received:")
        print(request.json)
        return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
