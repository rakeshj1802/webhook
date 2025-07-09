from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = 'POSEBOT123'  # Must exactly match Facebook Developer Verify Token

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def webhook():
    if request.method == 'HEAD':
        # Just respond OK to HEAD requests
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
        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
