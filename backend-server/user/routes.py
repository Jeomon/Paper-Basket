from application import db,bcrypt,user_datastore,signature,BadSignature,tasks
from flask_security import auth_token_required,roles_accepted,current_user
from flask import Blueprint,request,jsonify
from application.utilies import save_image,delete_image
from application.configuration import root_path
from user.models import User,Role,Request
from celery import group
from datetime import datetime
from category.models import Category
from product.models import Product
from order.models import Order
from secrets import token_hex
from base64 import b64decode
from io import BytesIO
from os import remove,listdir,path

user=Blueprint('user',__name__,url_prefix='/user',static_folder='static')

@user.get('/get')
@roles_accepted('Customer','Manager','Admin')
@auth_token_required
def get_user():
    user=current_user
    data={"id":user.id,
          "first_name": user.first_name,
          "last_name": user.last_name,
          "profile_image": user.profile_image,
          "gender": user.gender if user.gender else None,
          "dob": user.dob.strftime('%Y-%m-%d') if user.dob else None,
          "address": user.address,
          "mobile_no": user.mobile_no,
          "pin_code": user.pin_code,
          "email": user.email,
          "role": user.roles[0].name}
    return jsonify({'message': 'user found.','user': data})

@user.post('/forgot_password')
def user_forgot_password():
    formData=request.get_json()
    hostname=formData.get('hostname',None)
    port=formData.get('port',None)
    auth_token=formData.get('auth_token',None)
    verify_token=formData.get('verify_token',None)
    if verify_token is None:
        email=formData.get('email')
        user_exists=User.query.filter_by(email=email).first()
        if not user_exists:
            return jsonify({'message': 'User does not exist','reset':False})
        token=signature.dumps(email)
        tasks.send_reset_password.delay(user_exists.id,token,hostname,port)
        return jsonify({'message': 'Password reset email sent','reset': True})
    else:
        try:
            email=signature.loads(verify_token)
        except BadSignature:
            return jsonify({'message': 'Token is invalid','reset': False})
        user_exists=user_datastore.find_user(email=email)
        if user_exists.verify_auth_token(auth_token):
            return jsonify({'message': 'User is not authenticated','reset':False})
        password=formData.get('password')
        confirm_password=formData.get('confirm_password')
        if password!=confirm_password:
            return jsonify({'message':'Passwords does not match','reset':False})
        password_encrypt=bcrypt.generate_password_hash(password)
        User.query.filter_by(email=email).update({'password':password_encrypt})
        db.session.commit()
        return jsonify({'message':'New password is set','reset':True})

@user.get('/verify/reset_password/<confirm_token>')
def verify_reset_password(confirm_token):
    try:
        email=signature.loads(confirm_token)
    except BadSignature:
        return jsonify({'message': 'Token is invalid','token': None})
    user=user_datastore.find_user(email=email)
    token=user.get_auth_token()
    return jsonify({'message':'Token is valid','token':token})

@user.get('/verify/<confirm_token>')
def verify_user(confirm_token):
    try:
        email=signature.loads(confirm_token)
    except BadSignature:
        return jsonify({'message': 'Token is invalid','token': None})
    user=user_datastore.find_user(email=email)
    role=user.roles[0].name
    user.signin_date=datetime.date(datetime.today())
    user.active=True
    db.session.commit()
    token=user.get_auth_token()
    data={ "id": user.id,
           "first_name": user.first_name,
           "last_name": user.last_name,
           "profile_image": user.profile_image,
           "gender": user.gender,
           "dob": user.dob,
           "address": user.address,
           "mobile_no": user.mobile_no,
           "pin_code": user.pin_code,
           "email": user.email,
           "role": role.lower() }
    return jsonify({'message':f'Welcome back {user.first_name} {user.last_name}',
                    'token':token,'user': data})

@user.post('/<string:role>/signup')
def user_signup(role):
    formData=request.get_json()
    hostname=formData.get('hostname')
    port=formData.get('port')
    roles=[role.name for role in Role.query.all() if role.name!='Admin']
    user_exists=user_datastore.find_user(email=formData.get('email'))
    if user_exists:
        return jsonify({'message': 'User already exist','created': False})
    if role.capitalize() not in roles:
        return jsonify({'message': 'Invalid role specified','created': False})
    roles=user_datastore.find_role(role.capitalize())
    entry={ "fs_uniquifier": str(token_hex(10)),
            "first_name": formData.get('first_name'),
            "last_name": formData.get('last_name'),
            "profile_image": "default.png",
            "gender": formData.get('gender') if formData.get('gender') else None,
            "dob": datetime.strptime(formData.get('dob'),"%Y-%m-%d") if formData.get('dob') else None,
            "address": formData.get('address'),
            "mobile_no": formData.get('mobile_no'),
            "pin_code": formData.get('pin_code'),
            "email": formData.get('email'),
            "password": bcrypt.generate_password_hash(formData.get('password')),
            'signin_date': datetime.date(datetime.today()),
            "active": False,
            "roles": [roles],
            "products": [] }
    new_user=user_datastore.create_user(**entry)
    db.session.commit()
    if not new_user.active and role=='manager':
        return jsonify({'message': 'Waiting for admin approval','created': True})
    if not new_user.active and role=='customer':
        confirmation_token=signature.dumps(new_user.email)
        tasks.send_confirmation.delay(new_user.id, confirmation_token,hostname,port)
        return jsonify({'message':'Waiting for email confirmation','created': True})

@user.post('/<string:role>/signin')
def user_signin(role):
    formData=request.get_json()
    user=user_datastore.find_user(email=formData.get('email'))
    if not user:
        return jsonify({'message': 'User not found','access': False})
    if not user.is_active:
        if role=='manager':
            return jsonify({'message': 'Waiting for admin approval','access': False})
        if role=='customer':
            return jsonify({'message': 'Waiting for email verification','access': False})
    if not bcrypt.check_password_hash(user.password, formData.get('password')):
        return jsonify({'message': 'Wrong password','access': False})
    if user and (role.capitalize() not in [role.name for role in user.roles]):
        return jsonify({'message': 'User with invalid role','access': False})
    user.signin_date=datetime.date(datetime.today())
    db.session.commit()
    token=user.get_auth_token()
    data={ "id": user.id,
           "first_name": user.first_name,
           "last_name": user.last_name,
           "profile_image": user.profile_image,
           "gender": user.gender,
           "dob": user.dob,
           "address": user.address,
           "mobile_no": user.mobile_no,
           "pin_code": user.pin_code,
           "email": user.email,
           "role": role.lower() }
    return jsonify({'message':f'Welcome back {user.first_name} {user.last_name}',
                    'token':token,'access': True,'user': data})

@user.get('/<string:role>/signout')
@roles_accepted('Customer','Manager','Admin')
@auth_token_required
def user_signout(role):
    if role!='manager':
        return jsonify({'message':'user signed out.'})
    categories=Category.query.all()
    for category in categories:
        delete_image('/application/static',f'{category.name.lower()}.svg')
    temp_folder=listdir(path.abspath(root_path+path.join('/temp')))
    for filename in temp_folder:
        remove(path.abspath(root_path+path.join('/temp',filename)))
    return jsonify({'message':'all graphs are deleted and user signed out.'})

@user.put('/<string:role>/update')
@roles_accepted('Customer','Manager','Admin')
@auth_token_required
def user_update(role):
    formData=request.get_json()
    user=current_user
    carrier={}
    if formData.get('first_name') and user.first_name!=formData.get('first_name'):
        carrier['first_name']=formData.get('first_name')
    if formData.get('last_name') and user.last_name!=formData.get('last_name'):
        carrier['last_name']=formData.get('last_name')
    if formData.get('gender') and user.gender!=formData.get('gender'):
        carrier['gender']=formData.get('gender')
    if formData.get('dob') and user.dob!=formData.get('dob'):
        carrier['dob']=datetime.strptime(formData.get('dob'),"%Y-%m-%d")
    if formData.get('profile_image'):
        base64_image=b64decode(formData.get('profile_image'))
        profile_image=BytesIO(base64_image)
        delete_image('/user/static',current_user.profile_image)
        carrier['profile_image']=save_image('/user/static',profile_image,(125,125))
    if formData.get('address') and user.address!=formData.get('address'):
        carrier['address']=formData.get('address')
    if formData.get('mobile_no') and user.mobile_no!=formData.get('mobile_no'):
        carrier['mobile_no']=formData.get('mobile_no')
    if formData.get('pin_code') and user.pin_code!=formData.get('pin_code'):
        carrier['pin_code']=formData.get('pin_code')
    if formData.get('email') and user.email!=formData.get('email'):
        carrier['email']=formData.get('email')
    if carrier:
        User.query.filter_by(fs_uniquifier=current_user.fs_uniquifier).update(carrier)
        db.session.commit()
    data={"first_name": user.first_name,
          "last_name": user.last_name,
          "profile_image": user.profile_image,
          "gender": user.gender,
          "dob": user.dob,
          "address": user.address,
          "mobile_no": user.mobile_no,
          "pin_code": user.pin_code,
          "email": user.email,
          "role": role.lower()}
    return jsonify({'message':'Profile updated',
                    'user': data})

@user.delete('/<string:role>/delete')
@roles_accepted('Customer','Manager')
@auth_token_required
def user_delete(role):
    user=current_user
    email=user.email
    delete_image('/user/static',user.profile_image)
    user_datastore.delete_user(user)
    if "Manager" in user.roles:
        products=Product.query.filter(Product.user_id==current_user.id).all()
        for product in products:
            Product.query.filter(Product.id==product.id).delete()
            delete_image('/product/static',product.product_image)
    db.session.commit()
    return jsonify({'message': f'Your account {email} is deleted'})

@user.put('/<string:role>/update_password')
@roles_accepted('Customer','Manager','Admin')
@auth_token_required
def user_update_password(role):
    formData=request.get_json()
    user=current_user
    if formData.get('new_password')!=formData.get('confirm_password'):
        return jsonify({'message': 'Password do not match.','updated': False})
    if not bcrypt.check_password_hash(current_user.password,formData.get('current_password')):
        return jsonify({'message': 'Invalid password','updated': False})
    password=bcrypt.generate_password_hash(formData.get('new_password'))
    User.query.filter_by(fs_uniquifier=user.fs_uniquifier).update({'password': password})
    db.session.commit()
    return jsonify({'message': 'Password updated','updated': True})

@user.get('/manager/products')
@roles_accepted("Manager")
@auth_token_required
def get_manager_products():
    data=[]
    products=Product.query.filter(Product.user_id==current_user.id).all()
    for product in products:
        entry={ "id": product.id,
                "name": product.name,
                "product_image": product.product_image,
                "supplier": product.supplier,
                "origin": product.origin,
                "description": product.description,
                "expiry_date": product.expiry_date.strftime('%Y-%m-%d'),
                "inventory": product.inventory,
                "unit": product.unit,
                "price": product.price,
                "discount": product.discount,
                "category": product.category.name }
        data.append(entry)
    return jsonify({'message': 'manager specific products',
                    'products': data})

@user.get('/manager/trend_analysis')
@roles_accepted('Manager')
@auth_token_required
def trend_analysis_graphs():
    orders=Order.query.all()
    categories=Category.query.all()
    products_of_manager=Product.query.filter(Product.user_id==current_user.id).all()
    category_based_products=[]
    for order in orders:
        for product in products_of_manager:
            if order.name==product.name:
                data=tuple([order.name,order.category,int(order.order_date.month),int(order.quantity),order.unit,float(order.price)])
                category_based_products.append(data)
    category_tasks=[tasks.generate_graphs.s(category.name,category_based_products) for category in categories]
    group(category_tasks).delay()
    return jsonify({'message': 'graphs generated successfully'})

@user.get('/manager/trend_analysis/csv/<category>')
@roles_accepted('Manager')
@auth_token_required
def trend_analysis_csv(category):
    orders=Order.query.all()
    products_of_manager=Product.query.filter(Product.user_id==current_user.id).all()
    category_based_products=[]
    for product in products_of_manager:
        qty_sold,qty_sold_price=0,0
        for order in orders:
            if order.name==product.name and order.category.capitalize()==category.capitalize():
                qty_sold+=int(order.quantity)
                qty_sold_price+=float(order.price)
        qty_remain=product.inventory
        qty_remain_price=round(qty_remain*product.price)
        data=tuple([product.name,product.category.name,product.unit,
                    qty_sold,qty_sold_price,qty_remain,qty_remain_price])
        if product.category.name.capitalize()==category.capitalize():
            category_based_products.append(data)
    job=tasks.generate_csv.apply_async(args=[category_based_products])
    return jsonify({'message':'csv generating initiated',
                    'id':job.id})

@user.get('/manager/request/<id>')
@roles_accepted('Manager')
@auth_token_required
def get_request(id):
    request=Request.query.filter(Request.id==id).first()
    data={ 'id': request.id,
           'user_id': current_user.id,
           'name': f'{request.user.first_name} {request.user.last_name}',
           'request_date': request.request_date,
           'request_type': request.request_type,
           'status': request.status,
           'old_category_name': request.old_category_name,
           'new_category_name': request.new_category_name }
    return jsonify({'message': 'request obtained',
                    'request': data})  

@user.get('/manager/request/all')
@roles_accepted('Manager')
@auth_token_required
def manager_requests():
    requests=Request.query.filter_by(user_id=current_user.id).all()
    requests.reverse()
    data=[]
    for request_data in requests:
        entry={ 'id': request_data.id,
                'user_id': current_user.id,
                'name': f'{request_data.user.first_name} {request_data.user.last_name}',
                'request_date': request_data.request_date,
                'request_type': request_data.request_type,
                'status': request_data.status,
                'old_category_name': request_data.old_category_name,
                'new_category_name': request_data.new_category_name }
        data.append(entry)
    return jsonify({'message': 'Requests specific to manager',
                    'requests': data})

@user.post('/manager/request/add')
@roles_accepted('Manager')
@auth_token_required
def create_request():
    formData = request.get_json()
    entry={ 'request_type': formData.get('request_type').capitalize(),
        'request_date': datetime.date(datetime.now()),
        'new_category_name': formData.get('new_category_name'),
        'old_category_name': formData.get('old_category_name'),
        'status': 'Pending',
        'user': current_user }
    new_request=Request(**entry)
    db.session.add(new_request)
    data={ 'id': new_request.id,
           'user_id': current_user.id,
           'name': f'{new_request.user.first_name} {new_request.user.last_name}',
           'request_date': new_request.request_date,
           'request_type': new_request.request_type,
           'status': new_request.status,
           'old_category_name': new_request.old_category_name,
           'new_category_name': new_request.new_category_name }
    db.session.commit()
    return jsonify({'message': 'Request added',
                    'request': data})

@user.delete('/manager/request/delete/<id>')
@roles_accepted('Manager')
@auth_token_required
def delete_request(id):
    request_exists=Request.query.filter(Request.id==id).first()
    if not request_exists:
        return jsonify({'message': 'Request does not exist','deleted': False})
    Request.query.filter(Request.id==id).delete()
    db.session.commit()
    return jsonify({'message': 'Request deleted','deleted':True})

@user.get('/admin/request/all')
@roles_accepted('Admin')
@auth_token_required
def all_requests():
    requests=Request.query.filter(Request.status=='Pending').all()
    data=[]
    for request_data in requests:
        entry={
            'id': request_data.id,
            'user_id': request_data.user_id,
            'request_date': request_data.request_date,
            'request_type': request_data.request_type,
            'name': f'{request_data.user.first_name} {request_data.user.last_name}',
            'old_category_name': request_data.old_category_name,
            'new_category_name': request_data.new_category_name
        }
        data.append(entry)
    return jsonify({'message': 'all request',
                    'requests': data})

@user.put('/admin/request/approval')
@roles_accepted('Admin')
@auth_token_required
def category_approval():
    formData=request.get_json()
    id=formData.get('id')
    request_exists=Request.query.filter(Request.id==id).first()
    if not request_exists:
        return jsonify({'message': 'request does not exist'})
    status=formData.get('status')
    Request.query.filter(Request.id==id).update({Request.status:status})
    db.session.commit()
    return jsonify({'message': f'request has been {status.lower()}'})

@user.get('/admin/approval/managers')
@roles_accepted('Admin')
@auth_token_required
def all_managers_approval():
    role=user_datastore.find_role('Manager')
    managers=User.query.filter(User.roles.contains(role)).all()
    data=[]
    for manager in managers:
        if manager.active:
            continue
        entry={ 'id': manager.id,
                'first_name': manager.first_name,
                'last_name': manager.last_name,
                'email': manager.email,
                'mobile_no': manager.mobile_no,
                'pin_code': manager.pin_code }
        data.append(entry)
    return jsonify({'message': 'All managers for approval',
                    'managers': data})

@user.put('/admin/manager/approval')
@roles_accepted("Admin")
@auth_token_required
def manager_approval():
    formData=request.get_json()
    hostname=formData.get('hostname')
    port=formData.get('port')
    email=formData.get('email')
    status=formData.get('status')
    user_exists=user_datastore.find_user(email=email)
    if not user_exists:
        return jsonify({'message': 'User does not exist'})
    if status:
        User.query.filter(User.email==email).update({User.active:status})
        confirmation_token=signature.dumps(user_exists.email)
        tasks.send_confirmation.delay(user_exists.id,confirmation_token,hostname,port)
        msg={'message': 'Manager approved',
             'id': user_exists.id}
    else:
        user_datastore.delete_user(user=user_exists)
        msg={'message': 'Manager denied',
             'id': user_exists.id}
    db.session.commit()
    return jsonify(msg)
