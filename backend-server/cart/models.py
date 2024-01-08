from application import db
from user.models import User
from uuid import uuid4
from product.models import Product

class Cart(db.Model):
    __bind_key__='order'
    user_id=db.Column("user_id",db.String,db.ForeignKey(User.id),primary_key=True)
    product_id=db.Column("product_id",db.String,db.ForeignKey(Product.id),primary_key=True)
    quantity=db.Column("quantity",db.Integer)
    product=db.relationship(Product,backref='cart',lazy=True)
    user=db.relationship(User,backref='cart',lazy=True)

    def __init__(self,quantity,product,user):
        self.id=str(uuid4())
        self.quantity=quantity
        self.product=product
        self.user=user
