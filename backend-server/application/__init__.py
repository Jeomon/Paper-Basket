from flask_security import SQLAlchemyUserDatastore,Security
from itsdangerous import URLSafeSerializer,BadSignature
from application.configuration import Config
from flask_sqlalchemy import SQLAlchemy
from celery.schedules import crontab
from celery import Celery,Task
from flask_mail import Mail
from flask import Flask,jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from datetime import datetime
from secrets import token_hex
from . import tasks

app=Flask(__name__,static_folder='static')
app.config.from_object(Config)
mail= Mail(app)
db=SQLAlchemy(app)
cors=CORS(app)
bcrypt=Bcrypt(app)
cache=Cache(app)
signature=URLSafeSerializer(Config.SECRET_KEY)

from user.models import User,Role
from product.models import Product
from category.models import Category
from cart.models import Cart
from order.models import Order
from review.models import Review

user_datastore=SQLAlchemyUserDatastore(db,User,Role)
Security(app,user_datastore)

class ContextTask(Task):
    def __call__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)

celery=Celery(app.name,task_cls=ContextTask,broker='redis://localhost:6379/0',backend='redis://localhost:6379/1',
              enable_utc=False,broker_connection_retry_on_startup=True,timezone='Asia/Kolkata')
celery.config_from_object(app.config)
celery.set_default()
app.extensions['celery']=celery    

with app.app_context():
    db.create_all()
    db.create_all(bind_key=['product','order'])
    roles=[{'name': 'Customer', 'description': 'Can search, buy, review products and much more.'},
          {'name': 'Admin', 'description': 'Can monitor the activities in the application'},
          {'name': 'Manager', 'description': 'Add or remove also edit categories, products, etc.'}]
    for role in roles:
        if not user_datastore.find_role(role.get('name')):
            user_datastore.create_role(**role)
    db.session.commit()
    if not user_datastore.find_user(email='admin@paperbasket.com'):
        role=user_datastore.find_role('Admin')
        entry={
            'fs_uniquifier': str(token_hex(10)),'first_name': 'Admin',
            'last_name': '',"profile_image": "default.png",
            "gender":"male","dob": datetime.date(datetime.today()),
            "address": "","mobile_no": "","pin_code": "",
            "email": 'admin@paperbasket.com',"password": bcrypt.generate_password_hash('123'),
            'signin_date': datetime.date(datetime.today()),"active": True,
            "roles": [role],"products": []
        }
        user_datastore.create_user(**entry)
    db.session.commit()
    cache.clear()

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error_code': 401,
        'description': 'Authentication failed. Please check your credentials or obtain a valid token.'
    })

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'error_code': 403,
        'description': 'Access forbidden. You do not have the necessary permissions to access this resource.'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error_code': 404,
        'description': 'Resource not found. The requested resource could not be located on the server.'
    })


from application.routes import application
app.register_blueprint(application)
from user.routes import user
app.register_blueprint(user)
from category.routes import category
app.register_blueprint(category)
from product.routes import product
app.register_blueprint(product)
from cart.routes import cart
app.register_blueprint(cart)
from order.routes import order
app.register_blueprint(order)
from review.routes import review
app.register_blueprint(review)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='23',minute='39',day_of_month='*'),tasks.customer_monthly_report.s(),name='send mail to customers every first day of the month @ 06:00 hrs')
    sender.add_periodic_task(crontab(hour='18',minute='00',day_of_week='*'),tasks.customer_daily_inform.s(), name='send mail to customers every day @ 18:00 hrs')

