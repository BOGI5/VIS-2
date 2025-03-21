from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from flask import render_template, redirect, url_for, session, request 
from flask_login import login_user, logout_user, login_required, current_user 
import json
from app import db
from app.models.user import User, Customer
from config import Config as Auth
from app import app
from app.repositories.user import UserRepository, CustomerRepository

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return redirect(auth_url)


@app.route('/auth/handleGoogleLogin')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            UserRepository().create(user=user)
            user = UserRepository().find_by_email(email)
            login_user(user)
            return redirect(url_for('/'))
        return 'Could not fetch your information.'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_customer', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(first_name=data['first_name'], last_name=data['last_name'], phone=data['phone'], amount=data['amount'], family_status=data['family_status'], income=data['income'], egn=data['egn'], credit_expire=data['credit_expire'], address=data['address'], age=data['age'], job=data['job'], user_id=current_user.id)
    CustomerRepository().create(customer)
    return 'Customer created successfully!'

@app.route('/customers')
def customers():
    customers = CustomerRepository().all()
    return render_template('customers.html', customers=customers)

@app.route('/delete_customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    CustomerRepository().delete(id)
    return 'Customer deleted successfully!'
