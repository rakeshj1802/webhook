from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = 'POSEBOT123'  # Must match the token you enter on Facebook

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('Webhook verified successfully.')
            return challenge, 200
        else:
            return 'Verification failed', 403

    elif request.method == 'POST':
        data = request.json
        print('Received message:')
        print(data)
        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
