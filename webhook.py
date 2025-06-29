from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "your_verify_token"  # Set this yourself

@app.route('/webhook', methods=['GET'])
def verify():
    """Meta will verify your webhook when you add it in the dashboard."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified")
            return challenge, 200
        else:
            return "❌ Verification token mismatch", 403
    return "❌ Bad request", 400

@app.route('/webhook', methods=['POST'])
def webhook_event():
    """Handle webhook events like comments, likes, insights, etc."""
    data = request.json
    print("📩 Received webhook event:", data)

    # You can add logic to auto-analyze insights, store likes/comments, etc.
    return "✅ Event received", 200

if __name__ == '__main__':
    app.run(port=5000)
