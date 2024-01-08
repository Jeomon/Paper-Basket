from application import db
from uuid import uuid4
from user.models import User
from category.models import Category

class Product(db.Model):
    __bind_key__='product'
    id=db.Column("product_id",db.String,primary_key=True)
    name=db.Column("name",db.String,nullable=False)
    product_image=db.Column("product_image",db.String,nullable=True)
    supplier=db.Column("supplier",db.String,nullable=False)
    origin=db.Column("origin",db.String,nullable=False)
    description=db.Column("description",db.String,nullable=False)
    expiry_date=db.Column("expiry_date",db.Date,nullable=False)
    inventory=db.Column("inventory",db.Float,nullable=False)
    unit=db.Column("unit",db.String,nullable=False)
    price=db.Column("price",db.Float,nullable=False)
    discount=db.Column("discount",db.Float,nullable=True,default=0)
    category_id=db.Column("category_id",db.Integer,db.ForeignKey(Category.id))
    user_id=db.Column("user_id",db.String,db.ForeignKey(User.id))

    def __init__(self,name,product_image,supplier,origin,description,expiry_date,inventory,unit,price,discount,category,user):
        self.id=str(uuid4())
        self.name=name
        self.product_image=product_image
        self.supplier=supplier
        self.origin=origin
        self.description=description
        self.expiry_date=expiry_date
        self.inventory=inventory
        self.unit=unit
        self.price=price
        self.discount=discount
        self.category=category
        self.user=user