from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "POSTBOT123"  # Must match the token set in Meta dashboard

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("✅ Verified Webhook with Meta")
            return challenge, 200
        else:
            print("❌ Verification failed")
            return "Verification token mismatch", 403

    if request.method == 'POST':
        print("📩 Webhook Event Received:")
        print(request.json)
        return "Event received", 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
