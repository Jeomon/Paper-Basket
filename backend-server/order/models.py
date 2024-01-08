from application import db
from user.models import User
from uuid import uuid4

class Order(db.Model):
    __bind_key__='order'
    id=db.Column('order_id',db.String,primary_key=True)
    order_date=db.Column('date',db.Date,nullable=False)
    name=db.Column('name',db.String,nullable=False)
    category=db.Column('category',db.String,nullable=False)
    supplier=db.Column("supplier",db.String,nullable=False)
    quantity=db.Column("quantity",db.Integer,nullable=False)
    unit=db.Column('unit',db.String,nullable=False)
    price=db.Column("price",db.Float,nullable=False)
    user_id=db.Column("user_id",db.String,db.ForeignKey(User.id))
    user=db.relationship(User,backref='orders',lazy=True)

    def __init__(self,user,order_date,name,category,supplier,quantity,unit,price):
        self.id=str(uuid4())
        self.user=user
        self.order_date=order_date
        self.name=name
        self.category=category
        self.supplier=supplier
        self.quantity=quantity
        self.unit=unit
        self.price=price
