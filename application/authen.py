from flask_login import login_user,logout_user,current_user,login_required 
from flask import Flask , Blueprint,render_template,request,session,url_for,redirect
from authlib.integrations.flask_client import OAuth
from flask import current_app as app 
from .models import *
from .database import db 
from dotenv import load_dotenv 
import os 


# authen_blue=Blueprint('authen', __name__)

# @app.route('/login/')
# def login():
#     return rendar_template('login.html')

#load_dotenv()
oauth = OAuth()
oauth.init_app(app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo', 
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

@app.route('/') 

def home():
    #email = dict(session)['profile']['email']
    return render_template('home.html') 


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    #session["selected_role"] = "admin"
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri,prompt='select_account')  


@app.route("/login/student")
def login_student():
    google = oauth.create_client('google') 
    session["selected_role"] = "student"  # Session me role temporal save kiya
    redirect_uri = url_for("authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri,prompt='select_account') 

@app.route("/login/company")
def login_company():
    google = oauth.create_client('google') 
    session["selected_role"] = "company"  # Session me role temporal save kiya
    redirect_uri = url_for("authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, prompt='select_account')

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    google_id = user_info.get("id")  # Google ka unique ID
    print(user_info)
    print(google_id)
    email = user_info.get("email")
    name = user_info.get("name")
    user1 = User.query.filter_by(email=email).first()
    if not user1:
        role = session.get("selected_role")
        user1 = User(
            google_id=google_id,
            email=email,
            user_name=name,
            role=role 
        )
        db.session.add(user1)
        db.session.commit()
        login_user(user1)
    if not current_user.is_authenticated:
        role = session.get("selected_role") 
        user1.google_id=google_id 
        user1.role=role 
        db.session.commit()

    login_user(user1) 
    #session.clear()
    

    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    if user1.role=="company":
        return redirect(url_for("company")) 
    elif user1.role=="admin":
        return redirect(url_for("admin")) 
    else:
        return redirect(url_for("student"))





@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    logout_user() 
    return redirect('/')




            


