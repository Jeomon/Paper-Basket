from flask import Blueprint,request,jsonify
from application import db
from flask_security import auth_token_required,current_user,roles_accepted
from datetime import datetime
from review.models import Review
from product.models import Product

review=Blueprint('review',__name__,url_prefix='/review')

@review.get('/<product_id>/all')
def get_reviews_by_product(product_id):
    product_exists=Product.query.filter(Product.id==product_id).first()
    if not product_exists:
        return jsonify({'message':'product not found'})
    reviews=Review.query.filter(Review.product==product_exists).all()
    data=[]
    for review in reviews:
        entry={
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
        }
        data.append(entry)
    return jsonify({'message': 'reviews retrieved',
                    'reviews': data})

@review.post('/sentiment')
def sentiment():
    formData=request.get_json()
    user_id=formData.get('user_id')
    product_id=formData.get('product_id')
    like_count=formData.get('like_count')
    dislike_count=formData.get('dislike_count')
    review_exists=Review.query.filter_by(user_id=user_id,product_id=product_id).first()
    if not review_exists:
        return jsonify({'message':'Invalid review','sentimented':False})
    Review.query.filter_by(user_id=user_id,product_id=product_id).update({'dislikes':dislike_count,'likes':like_count})
    db.session.commit()
    sentiment={'dislike_count':dislike_count,'like_count':like_count}
    return jsonify({'message':'Sentiment added','sentiment':sentiment,'sentimented':True})

@review.post('/add')
@roles_accepted('Customer')
@auth_token_required
def add_review():
    formData=request.get_json()
    product_exists=Product.query.filter(Product.id==formData.get('id')).first()
    user_exists=Review.query.filter(Review.user==current_user,Review.product==product_exists).first()
    if 'Customer' not in current_user.roles:
        return jsonify({'message':'User has invalid role','added':False})
    if not product_exists:
        return jsonify({'message':'Product not found','added':False})
    if user_exists:
        return jsonify({'message':'Review from current user already exist','added':False})
    entry={ 'title': formData.get('title'),
            'posted_on': datetime.today(),
            'content': formData.get('content'),
            'rating': formData.get('rating'),
            'user': current_user,
            'product': product_exists,
            'likes': 0,
            'dislikes': 0 }
    add_review=Review(**entry)
    db.session.add(add_review)
    db.session.commit()
    data={ 'user_id': current_user.id,
           'product_id': product_exists.id,
           'name': f'{current_user.first_name} {current_user.last_name}',
           'image': current_user.profile_image,
           'posted_on': entry.get('posted_on'),
           'title': entry.get('title'),
           'content': entry.get('content'),
           'rating': entry.get('rating'),
           'likes': entry.get('likes'),
           'dislikes': entry.get('dislikes') }
    return jsonify({'message': 'Review added',
                    'review': data,'added': True})

@review.delete('/delete/<product_id>')
@roles_accepted('Customer')
def delete_review(product_id):
    user=Review.query.filter(Review.user==current_user).first()
    review_exists=Review.query.filter(Review.user_id==current_user.id,Review.product_id==product_id).first()
    if not review_exists:
        return jsonify({'message': 'Review does not exist','deleted':False})
    if not user:
        return jsonify({'message': 'Post does not belong to current user','deleted':False})
    Review.query.filter(Review.user_id==current_user.id,Review.product_id==product_id).delete()
    db.session.commit()
    return jsonify({'message': 'Review deleted','deleted':True})
