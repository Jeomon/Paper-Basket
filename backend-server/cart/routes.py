from flask import Blueprint,request,jsonify
from flask_security import auth_token_required,current_user,roles_required
from sqlalchemy import and_
from application import db
from cart.models import Cart
from order.models import Order
from product.models import Product
from datetime import datetime

cart=Blueprint('cart',__name__,url_prefix='/cart')

@cart.get('/products')
@roles_required('Customer')
@auth_token_required
def get_products():
    data=[]
    items=Cart.query.filter_by(user=current_user).all()
    for item in items:
        entry={ 'id': item.product.id,
                'name': item.product.name,
                'product_image': item.product.product_image,
                'category': item.product.category.name,
                'quantity': item.quantity,
                'unit': item.product.unit,
                'price': item.product.price,
                'discount': item.product.discount }
        data.append(entry)
    return jsonify({'message': 'cart products for the user',
                'products': data})

@cart.post('/add')
@roles_required('Customer')
@auth_token_required
def add_to_cart():
    formData=request.get_json()
    id=formData.get('id')
    if formData.get('quantity') is None:
        return jsonify({'message': 'Quantity not specified','added': False,'updated': False})
    product_exists=Product.query.filter(Product.id==id).first()
    if not product_exists:
        return jsonify({'message': 'Product not found','added':False,'updated': False})
    qty=formData.get('quantity')
    item_exists=Cart.query.filter(and_(Cart.user==current_user,Cart.product==product_exists)).first()
    if item_exists:
        if item_exists.quantity!=qty:
            item_exists.quantity=qty
            db.session.commit()
            data={  'id': id,
                    'name': product_exists.name,
                    'product_image': product_exists.product_image,
                    'category': product_exists.category.name,
                    'quantity': qty,
                    'unit': product_exists.unit,
                    'price': product_exists.price,
                    'discount': product_exists.discount }
            return jsonify({'message': 'Quantity updated','product':data,'added':False,'updated':True})
        else:
            return jsonify({'message': 'Already present in cart','added':False,'updated': False})
    else:
        entry={
             'quantity': qty,
             'user': current_user,
             'product': product_exists}
        new_item=Cart(**entry)
        db.session.add(new_item)
        db.session.commit()
        data={  'id': id,
                'name': product_exists.name,
                'product_image': product_exists.product_image,
                'category': product_exists.category.name,
                'quantity': qty,
                'unit': product_exists.unit,
                'price': product_exists.price,
                'discount': product_exists.discount }
        return jsonify({'message': 'Product added to the cart',
                        'product': data,'updated':False,'added':True})
    
@cart.delete('/order')
@roles_required('Customer')
@auth_token_required
def place_order():
    data=[]
    items=Cart.query.filter(Cart.user==current_user).all()
    for item in items:
        product=Cart.query.filter(and_(Cart.user==current_user,Cart.product==item.product)).first()
        qty=product.quantity
        entry={'user': current_user,
               'order_date': datetime.date(datetime.today()),
               'name': item.product.name,
               'category':item.product.category.name,
               'supplier': item.product.supplier,
               'quantity': product.quantity,
               'unit': item.product.unit,
               'price': round(item.product.price*(1-round(item.product.discount/100,2))*product.quantity,2)}
        data.append({'order_date': datetime.date(datetime.today()),
                     'name': item.product.name,
                     'category':item.product.category.name,
                     'supplier': item.product.supplier,
                     'quantity': product.quantity,
                     'unit': item.product.unit,
                     'price': round(item.product.price*(1-round(item.product.discount/100,2))*product.quantity,2)})
        product.product.inventory-=qty
        db.session.add(Order(**entry))
        Cart.query.filter_by(user=current_user,product=item.product).delete()
    db.session.commit()
    return jsonify({'message': 'Order placed successfully',
                    'orders': data})

@cart.delete('delete/<id>')
@roles_required('Customer')
@auth_token_required
def delete_from_cart(id):
    product_exists=Product.query.filter(Product.id==id).first()
    if not product_exists:
        return jsonify({'message': 'Product not found.'})
    item_exists=Cart.query.filter(and_(Cart.user==current_user,Cart.product==product_exists)).first()
    if not item_exists:
        return jsonify({'message': 'Item not found in cart'})
    db.session.delete(item_exists)
    db.session.commit()
    return jsonify({'message': 'Product removed from cart'})





    
