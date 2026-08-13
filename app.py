from flask import Flask, session 
from authlib.integrations.flask_client import OAuth
import os 
from dotenv import load_dotenv 
from flask_restful import Api 
from flask_login import LoginManager
from datetime import timedelta 
#from flask_bcrypt import Bcrypt
# from functools import wraps 


app=None
from application.database import db 
def create_app():
    app= Flask(__name__)
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY']=os.getenv("APP_SECRET_KEY")
    app.config['SESSION_COOKIE_NAME'] = os.getenv('SESSION_COOKIE_NAME')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['SQLALCHEMY_ENGINE_OPTIONS']={
        'pool_size':10, 'max_overflow':20, 'pool_timeout':30, 'pool_recycle':1800}

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    api=Api(app)
    db.init_app(app)
    #app.app_context().push()
    app.config['SESSION_COOKIE_SECURE'] = True     
    app.config['SESSION_COOKIE_HTTPONLY'] = True    
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = 'login'
    app.app_context().push()
    
    return app ,api

app,api=create_app()


# Blueprint ko Main App ke saath Register karein
# url_prefix: Har route ke aage '/auth' lag jayega
#app.register_blueprint(auth_bp, url_prefix='/auth')

from application.controller import * 
from application.authen import * 

# api.add_resource(Admin_dashboard,"/api/adminDashboard")
# api.add_resource(Signin,"/api/signCompany")

if __name__=="__main__":
    with app.app_context():
      db.create_all()
      admin=User.query.filter_by(role='admin').first() 
      if not admin:
        name=os.getenv('ADMIN_NAME')
        email=os.getenv('Admin_email')
        admin=User(user_name=name, email=email, role="admin")
        db.session.add(admin) 
        db.session.commit() 

    app.run(debug=True)






 



    
    


    
    

