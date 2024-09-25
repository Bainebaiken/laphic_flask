from flask import Blueprint, jsonify, request
from . import db  
from invix_app.models.article import Article  
from flask_jwt_extended import jwt_required
from functools import wraps
# Define a Blueprint for article-related routes
article_bp = Blueprint('article', __name__, url_prefix='/api/v1/articles')

# Admin required
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Create a new article
@article_bp.route('/register', methods=['POST'])
def create_article():
    data = request.get_json()
    title = data.get('title')
    text = data.get('text')
    video = data.get('video')
    image = data.get('image')  # Optional field
    user =data.get('user')
    date = data.get('date')

    category = data.get('category_id')

    if category == "Sports":
        category_id = 1
    elif category == "Technology":
        category_id = 2
    elif category == "Education":
        category_id = 3
    elif category == "Politics":
        category_id = 5
    elif category == "Entertainment":
        category_id = 4
    else:
        category_id = 1

    new_article = Article( title=title,text=text, video=video, image=image, user=user,date=date,category_id=category_id,)

    try:
        db.session.add(new_article)
        db.session.commit()
        return jsonify({'message': 'Article created successfully', 'id': new_article.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create article', 'error': str(e)}), 500

# Get all articles
@article_bp.route('/articles', methods=['GET'])
def get_all_articles():
    try:
        articles = Article.query.all() # .filter(category_id=1)
        article_list = []
        for article in articles:
            if article.category_id == 1:
                category = "Sports"
            elif article.category_id == 2:
                category = "Technology"
            elif article.category_id == 3:
                category = "Education"
            elif category == 5:
                category_id = "Politics"
            elif category == 4:
                category_id = "Entertainment"
            else:
                category = "Technology"

            article_list.append({
                'id': article.id,
                'title':article.title,
                'text': article.text,
                'video': article.video,
                'image': article.image,
                'user' :article.user,
                'date' :article.date,
                'category': category
            })
        return jsonify(article_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve articles', 'error': str(e)}), 500



# Get sports articles
@article_bp.route('/get_sports', methods=['GET'])
def get_sports_articles():
    try:
        articles = Article.query.all()
        article_list = []
        for article in articles:
            category = "Sports"
            if article.category_id == 1:
                article_list.append({
                    'id': article.id,
                    'title':article.title,
                    'text': article.text,
                    'video': article.video,
                    'image': article.image,
                    'user' :article.user,
                    'date' :article.date,
                    'category': category
                })
        print(len(article_list))
        return jsonify(article_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve articles', 'error': str(e)}), 500



# Get politics articles
@article_bp.route('/get_politics', methods=['GET'])
def get_politics_articles():
    try:
        articles = Article.query.all()
        article_list = []
        for article in articles:
            category = "Politics"
            if article.category_id == 5:
                article_list.append({
                    'id': article.id,
                    'title':article.title,
                    'text': article.text,
                    'video': article.video,
                    'image': article.image,
                    'user' :article.user,
                    'date' :article.date,
                    'category': category
                })
        return jsonify(article_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve articles', 'error': str(e)}), 500
    


# Get entertainment articles
@article_bp.route('/get_entertainment', methods=['GET'])
def get_entertainment_articles():
    try:
        articles = Article.query.all()
        article_list = []
        for article in articles:
            category = "Entertainment"
            if article.category_id == 4:
                article_list.append({
                    'id': article.id,
                    'title':article.title,
                    'text': article.text,
                    'video': article.video,
                    'image': article.image,
                    'user' :article.user,
                    'date' :article.date,
                    'category': category
                })
        return jsonify(article_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve articles', 'error': str(e)}), 500


# Get a single article by ID
@article_bp.route('/<int:id>', methods=['GET'])
def get_article(id):
    try:
        article = Article.query.get(id)
        if not article:
            return jsonify({'message': 'Article not found'}), 404

        return jsonify({
            'id': article.id,
            'title':article.title,
            'text': article.text,
            'video': article.video,
            'image': article.image,
            'user' :article.user,
            'date' :article.date
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve article', 'error': str(e)}), 500


# Update an article by ID
@article_bp.route('/<int:id>', methods=['PUT'])
def update_article(id):
    data = request.get_json()
    try:
        article = Article.query.get(id)
        if not article:
            return jsonify({'message': 'Article not found'}), 404

        article.title = data.get('title', article.title)
        article.text = data.get('text', article.text)
        article.video = data.get('video', article.video)
        article.image = data.get('image', article.image)
        article.date = data.get('date', article.date)
        article.user = data.get('user', article.user)
        db.session.commit()
        return jsonify({'message': 'Article updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update article', 'error': str(e)}), 500


# Delete an article by ID
@article_bp.route('/delete_article', methods=['DELETE'])
# @admin_required
def delete_article():
    try:
        
        data = request.get_json()

        email = data.get('email')
        print(email)
        id = data.get('id')
        print(id)

        article = Article.query.get(id)

        if not article:
            return jsonify({'message': 'Article not found'}), 404

        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Article deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete article', 'error': str(e)}), 500
