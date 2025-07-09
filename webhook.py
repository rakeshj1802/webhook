from flask import Flask, redirect, request
import requests

app = Flask(__name__)

# Replace these with your App details:
APP_ID = '1626542948040488'
APP_SECRET = '7a856c2d974e1b26fe25b257f24c506a'
REDIRECT_URI = 'https://webhook-g6zu.onrender.com/login/callback'  # Your public callback URL

@app.route('/')
def home():
    return '''
        <h2>Instagram Business Login</h2>
        <a href="/login">Login with Instagram</a>
    '''

@app.route('/login')
def login():
    # Redirect user to Instagram OAuth dialog
    oauth_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user_profile,user_media"
        f"&response_type=code"
    )
    return redirect(oauth_url)

@app.route('/login/callback')
def instagram_callback():
    # Instagram redirects here after login with 'code' in query params
    code = request.args.get('code')
    if not code:
        return 'Authorization failed.', 400

    # Exchange code for access token
    token_url = "https://api.instagram.com/oauth/access_token"
    payload = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        return f"Failed to get access token: {response.text}", 400

    data = response.json()
    access_token = data.get('access_token')
    user_id = data.get('user_id')

    return f'''
        <h3>Access Token Received!</h3>
        <p><strong>Access Token:</strong> {access_token}</p>
        <p><strong>User ID:</strong> {user_id}</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
