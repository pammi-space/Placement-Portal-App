from flask import Flask ,redirect, url_for, request,render_template,session,make_response
from flask import current_app as app 
from flask_restful import Api ,Resource
from flask_login import UserMixin,login_user,logout_user,login_manager,current_user,login_required
from .models import * 
from flask_bcrypt import Bcrypt
from .database import db 
from functools import wraps
#from flask import flask_sqlalchemy 
#from app import bcrypt




@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            return {"message": "Unauthorized access"}, 403
        return func(*args, **kwargs)
    return wrapper

  #route flask_restful 
@app.route('/adminDash')
@login_required
def admin():
    return "<h4>this is admin dashboard</h4>" 

@app.route("/companyDash") 
@login_required
def company():
    return "<h4>this is company dashboard</h4>"

@app.route("/student_dash")
@login_required
def student():
    return "<h4>this is student dashboard</h4>"
