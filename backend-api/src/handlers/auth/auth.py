from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)

load_dotenv()

oauth.register(
    name='cognito',
    client_id=os.environ["COGNITO_APP_CLIENT_ID"],
    client_secret=os.environ["COGNITO_APP_CLIENT_SECRET"],
    api_base_url=f"https://{os.environ['COGNITO_DOMAIN']}",
    authorize_url=f"https://{os.environ['COGNITO_DOMAIN']}/oauth2/authorize",
    access_token_url=f"https://{os.environ['COGNITO_DOMAIN']}/oauth2/token",
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
def index():
    user = session.get('user')
    return f"Hello {user['email']}" if user else '<a href="/login">Login</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True).replace("localhost", "127.0.0.1")
    return oauth.cognito.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.cognito.authorize_access_token()
    print("TOKEN:", token)  # <--- this logs your token to the terminal
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

