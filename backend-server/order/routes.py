from flask import Blueprint,jsonify
from flask_security import auth_token_required,roles_required,current_user
from order.models import Order

order=Blueprint('order',__name__,url_prefix='/orders',static_folder='static')

@order.get('/all')
@roles_required('Customer')
@auth_token_required
def get_customer_orders():
    data=[]
    orders=Order.query.filter_by(user=current_user).all()
    for order in orders:
        entries={
            "order_date": order.order_date,
            "name": order.name,
            "category": order.category,
            "supplier": order.supplier,
            "quantity": order.quantity,
            "unit": order.unit,
            "price": order.price
        }
        data.append(entries)
    return jsonify({'message': 'orders made by the user',
                    'orders': data})