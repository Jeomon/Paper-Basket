from flask_security import UserMixin,RoleMixin
from uuid import uuid4
from application import db

class User(db.Model,UserMixin):
    id=db.Column("user_id",db.String,primary_key=True)
    fs_uniquifier=db.Column("fs_uniquifier",db.String,nullable=False,unique=True)
    first_name=db.Column("first_name",db.String,nullable=False)
    last_name=db.Column("last_name",db.String,nullable=False)
    profile_image=db.Column("profile_image",db.String,nullable=True)
    gender=db.Column("gender",db.String,nullable=True)
    dob=db.Column("dob",db.Date,nullable=True)
    address=db.Column("address",db.String,nullable=False)
    mobile_no=db.Column("mobile_no",db.Integer,nullable=False)
    pin_code=db.Column("pin_code",db.Integer,nullable=False)
    email=db.Column("email",db.String,nullable=False,unique=True)
    password=db.Column("password",db.String,nullable=False)
    signin_date=db.Column("signin_date",db.Date,nullable=False)
    active=db.Column("active",db.Boolean,default=True)
    roles=db.relationship("Role",secondary='association',lazy=True)
    products=db.relationship("Product",backref='user',lazy=True)

    def __init__(self,fs_uniquifier,first_name,last_name,profile_image,gender,dob,address,mobile_no,pin_code,email,password,signin_date,active,roles,products):
        self.id=str(uuid4())
        self.fs_uniquifier=fs_uniquifier
        self.first_name=first_name
        self.last_name=last_name
        self.profile_image=profile_image
        self.gender=gender
        self.dob=dob
        self.address=address
        self.mobile_no=mobile_no
        self.pin_code=pin_code
        self.email=email
        self.password=password
        self.signin_date=signin_date
        self.active=active
        self.roles=roles
        self.products=products

class Role(db.Model,RoleMixin):
    id=db.Column("role_id",db.String,primary_key=True)
    name=db.Column("name",db.String,nullable=False)
    description=db.Column("description",db.String,nullable=False)

    def __init__(self,name,description):
        self.id=str(uuid4())
        self.name=name
        self.description=description

class Association(db.Model):
    user_id=db.Column("user_id",db.String,db.ForeignKey(User.id),primary_key=True)
    role_id=db.Column("role_id",db.String,db.ForeignKey(Role.id),primary_key=True)

class Request(db.Model):
    id=db.Column("id",db.String,primary_key=True)
    user_id=db.Column("user_id",db.String,db.ForeignKey(User.id),primary_key=True)
    request_type=db.Column("request_type",db.String,nullable=False)
    request_date=db.Column("request_date",db.Date,nullable=False)
    new_category_name=db.Column("new_category_name",db.String)
    old_category_name=db.Column("old_category_name",db.String)
    status=db.Column("status",db.String)
    user=db.relationship(User,backref='requests',lazy=True)

    def __init__(self,request_type,request_date,user,status,new_category_name=None,old_category_name=None):
        self.id=str(uuid4())
        self.request_type=request_type
        self.request_date=request_date
        self.new_category_name=new_category_name
        self.old_category_name=old_category_name
        self.status=status
        self.user=user


        