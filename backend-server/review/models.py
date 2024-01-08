from application import db
from user.models import User
from product.models import Product
from datetime import datetime

class Review(db.Model):
    __bind_key__='product'
    user_id=db.Column("user_id",db.String,db.ForeignKey(User.id),primary_key=True)
    product_id=db.Column("product_id",db.String,db.ForeignKey(Product.id),primary_key=True)
    title=db.Column("title",db.String,nullable=False)
    posted_on=db.Column("posted_date",db.DateTime,nullable=False,default=datetime.today())
    content=db.Column("content",db.String,nullable=False)
    rating=db.Column("rating",db.Integer,nullable=False)
    likes=db.Column("likes",db.Integer,default=0)
    dislikes=db.Column("dislikes",db.Integer,default=0)
    product=db.relationship(Product,backref="reviews",lazy=True)
    user=db.relationship(User,backref="reviews",lazy=True)

    def __init__(self,title,posted_on,content,rating,likes,dislikes,user,product):
        self.title=title
        self.posted_on=posted_on
        self.content=content
        self.rating=rating
        self.likes=likes
        self.dislikes=dislikes
        self.user=user
        self.product=product