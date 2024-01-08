from flask import Blueprint,request,jsonify
from flask_security import auth_token_required,roles_required
from category.models import Category
from product.models import Product
from application import db
from application.utilies import delete_image

category=Blueprint('category',__name__,url_prefix='/category')

@category.get('/<id>')
@auth_token_required
def get_category(id):
    category=Category.query.filter(Category.id==id).first()
    data={ 'id': category.id,
           'name': category.name,
           'consumable': category.consumable,
           'vegetarian': category.vegetarian }
    return jsonify({'message': 'category found.',
                    'category': data})

@category.get('/all')
def get_categories():
    data=[]
    categories=Category.query.all()
    for category in categories:
        entry={
            'id': category.id,
            'name': category.name,
            'consumable': category.consumable,
            'vegetarian': category.vegetarian
        }
        data.append(entry)
    return jsonify({'message': 'all categories.',
                    'categories': data })

@category.post('/add')
@roles_required("Admin")
@auth_token_required
def add_category():
    formData=request.get_json()
    category_exists=Category.query.filter(Category.name==formData.get('name')).first()
    if category_exists:
        return jsonify({'message': 'Category already exist.','added': False})
    entry={ 'name': formData.get('name'),
            'consumable': formData.get('consumable'),
            'vegetarian': formData.get('vegetarian') }
    new_category=Category(**entry)
    db.session.add(new_category)
    db.session.commit()
    data={ 'id': new_category.id,
           'name': new_category.name,
           'consumable': new_category.consumable,
           'vegetarian': new_category.vegetarian }
    return jsonify({'message': f'{new_category.name} added','category':data,'added': True})

@category.put('/update/<id>')
@roles_required("Admin")
@auth_token_required
def update_category(id):
    formData=request.get_json()
    category_exists=Category.query.filter(Category.id==id).first()
    if not category_exists:
        return jsonify({'message': 'Category does not exist','updated':False})
    carrier={}
    if formData.get('new_name')!=category_exists.name:
        carrier['name']=formData.get('new_name')
    if formData.get('consumable')!=category_exists.consumable:
        carrier['consumable']=formData.get('consumable')
    if formData.get('vegetarian')!=category_exists.vegetarian:
        carrier['vegetarian']=formData.get('vegetarian')
    if carrier:
        Category.query.filter(Category.id==id).update(carrier)
        db.session.commit()
        data={ 'id': id,
               'name': formData.get('new_name'),
               'consumable': formData.get('consumable'),
               'vegetarian': formData.get('vegetarian') }
        return jsonify({'message': 'Category updated.','category':data,'updated':True})
    return jsonify({'message': 'No changes found','updated':False})

@category.delete('/delete/<id>')
@roles_required("Admin")
@auth_token_required
def delete_category(id):
    category_exists=Category.query.filter(Category.id==id).first()
    if not category_exists:
        return jsonify({'message': 'Category does not exist','deleted':False})
    Category.query.filter(Category.id==id).delete()
    products=category_exists.products
    for product in products:
        Product.query.filter(Product.id==product.id).delete()
        delete_image('/product/static',product.product_image)
    db.session.commit()
    return jsonify({'message': 'Category deleted','deleted':True})