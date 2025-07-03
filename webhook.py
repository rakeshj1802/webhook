from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "thinkfinex_webhook_2025"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    if request.method == "POST":
        data = request.json
        print("📩 Webhook event:", data)
        return "Event received", 200
