from .database import db 
from flask_login import UserMixin,login_user,logout_user,login_manager,current_user
from datetime import datetime,date 

#user class
class User(db.Model,UserMixin):
    user_id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    user_name=db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    #password=db.Column(db.String(45), nullable=False)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    role=db.Column(db.String, nullable=False)  #admin, company ,student
    
    def get_id(self):
        return str(self.user_id)


class Company(db.Model):
    ceo_name=db.column(db.string(78),nullable=False)
    company_name=db.Column(db.String(100),nullable=False,unique=True)
    company_id=db.Column(db.String, primary_key=True)
    #company_type=db.column(db.string, nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    website=db.Column(db.String,nullable=False,unique=True)
    hr_cont=db.Column(db.Integer,nullable=False,unique=True)
    status=db.Column(db.String,nullable=False, default='pending')  #approved,pending,reject
    placement_drive=db.relationship('Placement_drive',back_populates='company')

class Student(db.Model):
    name=db.Column(db.String(100))
    email=db.Column(db.String(100),nullable=False,unique=True)
    education=db.Column(db.String,nullable=False)
    #resume=db.column(db.string,unique=True)
    student_id=db.Column(db.String,unique=True,primary_key=True )
    contact=db.Column(db.Integer,unique=True)
    application=db.relationship('Application',back_populates='student')
    status=db.Column(db.String,nullable=False,default='approve') # approve, blacklist 

class Placement_drive(db.Model):
    drive_id=db.Column(db.String,unique=True,primary_key=True )
    posting_date=db.Column(db.date, nullable=False, default=date.today)
    company_id=db.Column(db.String(100),db.ForeignKey('company.company_id'), nullable=False)
    job_title=db.Column(db.String,nullable=False)
    job_description=db.Column(db.String,nullable=False) 
    eligibility=db.Column(db.String,nullable=False)
    application_deadline=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String,nullable=False, default='pending')  #approved,pending,reject
    applicant=db.relationship('Application',back_populates='placement')
    company=db.relationship('Company',back_populates='placement_drive')


class Application(db.Model):
    application_id=db.Column(db.String,unique=True,primary_key=True )
    student_id=db.Column(db.String,db.ForeignKey('student.student_id'), nullable=False )
    drive_id=db.Column(db.String,db.ForeignKey('placement_drive.drive_id'), nullable=False)
    application_date=db.Column(db.date,nullable=False, default=date.today) 
    status=db.Column(db.String,nullable=False,default='pending') #pending, reject,approved
    student=db.relationship('Student', back_populates='application')  
    placement=db.relationship('Placement_drive', back_populates='applicant') 


