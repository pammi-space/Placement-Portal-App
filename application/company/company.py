from flask import Flask ,redirect, url_for, request,render_template,session,make_response
from flask import current_app as app 
from flask_restful import Api ,Resource
from flask_login import UserMixin,login_user,logout_user,login_manager,current_user,login_required
from .models import * 
from flask_bcrypt import Bcrypt
from .database import db 
from functools import wraps

# @app.route("/companyDash") 
# @login_required
class Company(Resource):
    def get():
        if current_user.role=='company':
            email=current_user.email
            comp=Company.query.filter_by(email=email).first()
            
            
    