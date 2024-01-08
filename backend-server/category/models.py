from application import db
from uuid import uuid4

class Category(db.Model):
    __bind_key__='product'
    id=db.Column("category_id",db.String,primary_key=True)
    name=db.Column("name",db.String,nullable=False)
    consumable=db.Column("consumable",db.String,nullable=False)
    vegetarian=db.Column("vegetarian",db.String,nullable=False)
    products=db.relationship("Product",backref="category",lazy=True)

    def __init__(self,name,consumable,vegetarian):
        self.id=str(uuid4())
        self.name=name
        self.consumable=consumable
        self.vegetarian=vegetarian

