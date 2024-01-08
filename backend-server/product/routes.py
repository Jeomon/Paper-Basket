from flask import Blueprint,request,jsonify
from flask_security import auth_token_required,roles_accepted,current_user
from product.models import Product
from category.models import Category
from review.models import Review
from application.utilies import save_image,delete_image
from application import db,cache
from base64 import b64decode
from datetime import datetime
from io import BytesIO

product=Blueprint('product',__name__,url_prefix='/product',static_folder='static')

@product.get('/<id>')
@cache.cached(timeout=10)
def get_product(id):
    product=Product.query.filter(Product.id==id).first()
    if not product:
        return jsonify({'message': 'product not found.'})
    reviews=Review.query.filter(Review.product==product).all()
    if len(reviews)!=0:
        rating=round(sum([review.rating for review in reviews])/len(reviews),2)
    else:
        rating=0
    detailed_rating={1:0,2:0,3:0,4:0,5:0}
    stars=[1,2,3,4,5]
    for star in stars:
        for review in reviews:
            if review.rating==star:
                detailed_rating[star]+=1
    data={ "id": product.id,
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
           "category": product.category.name,
           "rating": rating,
           "ratings": detailed_rating,
           "reviews": [{
           'user_id': review.user_id,
           'name': f'{review.user.first_name} {review.user.last_name}',
           'image': review.user.profile_image,
           'posted_on': review.posted_on,
           'title': review.title,
           'content': review.content,
           'rating': review.rating,
           'likes': review.likes,
           'dislikes': review.dislikes
            }for review in reviews]}
    return jsonify({'message': 'product found.',
                    'product': data})

@product.get('/all')
@cache.cached(timeout=10)
def get_products():
    data=[]
    products=Product.query.all()
    products.reverse()
    for product in products:
        reviews=Review.query.filter(Review.product==product).all()
        if len(reviews)!=0:
            rating=round(sum([review.rating for review in reviews])/len(reviews),2)
        else:
            rating=0
        detailed_rating={1:0,2:0,3:0,4:0,5:0}
        stars=[1,2,3,4,5]
        for star in stars:
            for review in reviews:
                if review.rating==star:
                    detailed_rating[star]+=1
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
                "rating": rating,
                "ratings": detailed_rating,
                "category": product.category.name,
                "vegetarian":True if product.category.vegetarian else False,
                "reviews": [{
                'user_id': review.user_id,
                'product_id': review.product_id,
                'name': f'{review.user.first_name} {review.user.last_name}',
                'image': review.user.profile_image,
                'posted_on': review.posted_on,
                'title': review.title,
                'content': review.content,
                'rating': review.rating,
                'likes': review.likes,
                'dislikes': review.dislikes
                }for review in reviews]}
        data.append(entry)
    return jsonify({'message': 'all products.',
                    'products': data})

@product.post('/add')
@roles_accepted("Manager")
@auth_token_required
def add_product():
    formData=request.get_json()
    detailed_rating={1:0,2:0,3:0,4:0,5:0}
    product_exists=Product.query.filter(Product.name==formData.get("name")).first()
    if product_exists:
        return jsonify({'message': 'Product already exist','added': False})
    base64_image=b64decode(formData.get('product_image').get('file'))
    image_type=formData.get('product_image').get('type')
    image_types=['image/jpeg', 'image/png','image/jpg']
    if base64_image and (image_type in image_types):
        product_image_binary=BytesIO(base64_image)
        product_image=save_image('/product/static',product_image_binary,(500,500))
    else:
        product_image='no-image.png'
    if not int(formData.get("inventory"))>=0:
        return jsonify({'message': 'Invalid inventory','added': False}) 
    category=Category.query.filter(Category.name==formData.get("category")).first()
    entry={ "name": formData.get("name"),
            "product_image": product_image,
            "category": category,
            "inventory": formData.get("inventory"),
            "unit": formData.get("unit"),
            "supplier": formData.get("supplier"),
            "origin": formData.get("origin"),
            "expiry_date": datetime.strptime(formData.get('expiry_date'),"%Y-%m-%d"),
            "price": formData.get("price"),
            "discount": formData.get("discount"),
            "description": formData.get("description"),
            "user": current_user }
    new_product=Product(**entry)
    db.session.add(new_product)
    data={ "id": new_product.id,
           "name": new_product.name,
           "product_image": new_product.product_image,
           "supplier": new_product.supplier,
           "origin": new_product.origin,
           "description": new_product.description,
           "expiry_date": new_product.expiry_date.strftime('%Y-%m-%d'),
           "inventory": new_product.inventory,
           "unit": new_product.unit,
           "price": new_product.price,
           "discount": new_product.discount,
           "category": new_product.category.name,
           "vegetarian":True if new_product.category.vegetarian else False,
           "rating": 0,
           "ratings": detailed_rating,
           "reviews": []}
    db.session.commit()
    return jsonify({'message': f'{new_product.name} added','added': True,
                    'product': data})

@product.put('/update/<id>')
@roles_accepted("Manager")
@auth_token_required
def update_product(id):
    formData=request.get_json()
    product_exists=Product.query.filter(Product.id==id).first()
    if not product_exists:
        return jsonify({'message': 'Product does not exist.','updated': False})
    if product_exists.user!=current_user:
        return jsonify({'message': 'Product does not belong to current manager','updated':False})
    image_types=['image/jpeg', 'image/png','image/jpg']
    carrier={}
    if (formData.get('product_image').get('type') in image_types) and formData.get('product_image').get('file'):
        base64_image=b64decode(formData.get('product_image').get('file'))
        product_image=BytesIO(base64_image)
        delete_image('/product/static',product_exists.product_image)
        carrier['product_image']=save_image('/product/static',product_image,(500,500))
    if formData.get('inventory')!=product_exists.inventory and int(formData.get('inventory'))>=0:
        carrier['inventory']=formData.get('inventory')
    if formData.get('supplier')!=product_exists.supplier:
        carrier['supplier']=formData.get('supplier')
    if formData.get('origin')!=product_exists.origin:
        carrier['origin']=formData.get('origin')
    if formData.get('expiry_date')!=product_exists.expiry_date:
        carrier['expiry_date']=datetime.strptime(formData.get('expiry_date'),"%Y-%m-%d")
    if formData.get('price')!=product_exists.price:
        carrier['price']=formData.get('price')
    if formData.get('discount')!=product_exists.discount:
        carrier['discount']=formData.get('discount')
    if carrier:
        Product.query.filter(Product.id==id).update(carrier)
        product=Product.query.filter(Product.id==id).first()
        reviews=Review.query.filter(Review.product==product).all()
        if len(reviews)!=0:
            rating=round(sum([review.rating for review in reviews])/len(reviews),2)
        else:
            rating=0
        detailed_rating={1:0,2:0,3:0,4:0,5:0}
        stars=[1,2,3,4,5]
        for star in stars:
            for review in reviews:
                if review.rating==star:
                    detailed_rating[star]+=1
        data={ "id": product.id,
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
                "rating": rating,
                "ratings": detailed_rating,
                "category": product.category.name,
                "vegetarian":True if product.category.vegetarian else False,
                "reviews": [{
                'user_id': review.user_id,
                'product_id': review.product_id,
                'name': f'{review.user.first_name} {review.user.last_name}',
                'image': review.user.profile_image,
                'posted_on': review.posted_on,
                'title': review.title,
                'content': review.content,
                'rating': review.rating,
                'likes': review.likes,
                'dislikes': review.dislikes
                }for review in reviews]}
        db.session.commit()
        return jsonify({'message': 'Product updated','product':data,'updated':True})
    else:
        return jsonify({'message': 'No changes found','updated':False})
    
@product.delete('/delete/<id>')
@roles_accepted("Manager")
@auth_token_required
def delete_product(id):
    product_exists = Product.query.filter(Product.id==id).first()
    if not product_exists:
        return jsonify({'message': 'Product does not exist.','deleted':False})
    delete_image('/product/static',product_exists.product_image)
    Product.query.filter(Product.id==id).delete()
    db.session.commit()
    return jsonify({'message': 'Product deleted','deleted':True})

