from flask import Blueprint, request, jsonify
from invix_app.extensions import db
from invix_app.models.posts import Posts  
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Define a Blueprint for post-related routes
post_bp = Blueprint('post', __name__, url_prefix='/api/v1/posts')  # Adjusted Blueprint definition

# Create a new post
@post_bp.route('/register', methods=['POST'])  
def create_post():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        user_id = data.get('user_id')
        comment = data.get('comment')
        blog = data.get('blog')

        new_post = Posts(title=title, description=description, user_id=user_id,
                        comment=comment, blog=blog)

        db.session.add(new_post)
        db.session.commit()

        return jsonify({'message': 'Post created successfully', 'id': new_post.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create post', 'error': str(e)}), 500

# Get all posts
@post_bp.route('/', methods=['GET'])
def get_all_posts():
    try:
        posts = Post.query.all()
        posts_list = []
        for post in posts:
            posts_list.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'user_id': post.user_id,
                'comment': post.comment,
                'blong': post.blong,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else None
            })
        return jsonify(posts_list), 200

    except Exception as e:
        return jsonify({'message': 'Failed to retrieve posts', 'error': str(e)}), 500

# Get a single post by ID
@post_bp.route('/<int:id>', methods=['GET'])
def get_post(id):
    try:
        post = Post.query.get(id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        return jsonify({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'user_id': post.user_id,
            'comment': post.comment,
            'blong': post.blong,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else None
        }), 200

    except Exception as e:
        return jsonify({'message': 'Failed to retrieve post', 'error': str(e)}), 500

# Update a post by ID
@post_bp.route('/<int:id>', methods=['PUT'])
def update_post(id):
    try:
        data = request.get_json()
        post = Post.query.get(id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        post.title = data.get('title', post.title)
        post.description = data.get('description', post.description)
        post.user_id = data.get('user_id', post.user_id)
        post.comment = data.get('comment', post.comment)
        post.blong = data.get('blong', post.blong)
        post.updated_at = datetime.now()

        db.session.commit()
        return jsonify({'message': 'Post updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update post', 'error': str(e)}), 500

# Delete a post by ID
@post_bp.route('/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        post = Post.query.get(id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete post', 'error': str(e)}), 500



# from flask import Blueprint, request, jsonify
# from invix_app.extensions import db
# from invix_app.models.posts import Posts  # Adjusted model import
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from datetime import datetime

# # Define a Blueprint for post-related routes
# post_bp = Blueprint('post', __name__, url_prefix='/api/v1/posts')  # Adjusted Blueprint definition

# # Create a new post
# @post_bp.route('/register', methods=['POST'])
# def create_post():
#     try:
#         data = request.get_json()
#         title = data.get('title')
#         description = data.get('description')
#         user_id = data.get('user_id')
#         comment = data.get('comment')
#         blong = data.get('blong')

#         new_post = Post(title=title, description=description, user_id=user_id,
#                         comment=comment, blong=blong)

#         db.session.add(new_post)
#         db.session.commit()

#         return jsonify({'message': 'Post created successfully', 'id': new_post.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create post', 'error': str(e)}), 500

# # Get all posts
# @post_bp.route('/', methods=['GET'])
# def get_all_posts():
#     try:
#         posts = Post.query.all()
#         posts_list = []
#         for post in posts:
#             posts_list.append({
#                 'id': post.id,
#                 'title': post.title,
#                 'description': post.description,
#                 'user_id': post.user_id,
#                 'comment': post.comment,
#                 'blong': post.blong,
#                 'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#                 'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else None
#             })
#         return jsonify(posts_list), 200

#     except Exception as e:
#         return jsonify({'message': 'Failed to retrieve posts', 'error': str(e)}), 500

# # Get a single post by ID
# @post_bp.route('/<int:id>', methods=['GET'])
# def get_post(id):
#     try:
#         post = Post.query.get(id)
#         if not post:
#             return jsonify({'message': 'Post not found'}), 404

#         return jsonify({
#             'id': post.id,
#             'title': post.title,
#             'description': post.description,
#             'user_id': post.user_id,
#             'comment': post.comment,
#             'blong': post.blong,
#             'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else None
#         }), 200

#     except Exception as e:
#         return jsonify({'message': 'Failed to retrieve post', 'error': str(e)}), 500

# # Update a post by ID
# @post_bp.route('/<int:id>', methods=['PUT'])
# def update_post(id):
#     try:
#         data = request.get_json()
#         post = Post.query.get(id)
#         if not post:
#             return jsonify({'message': 'Post not found'}), 404

#         post.title = data.get('title', post.title)
#         post.description = data.get('description', post.description)
#         post.user_id = data.get('user_id', post.user_id)
#         post.comment = data.get('comment', post.comment)
#         post.blong = data.get('blong', post.blong)
#         post.updated_at = datetime.now()

#         db.session.commit()
#         return jsonify({'message': 'Post updated successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to update post', 'error': str(e)}), 500

# # Delete a post by ID
# @post_bp.route('/<int:id>', methods=['DELETE'])
# def delete_post(id):
#     try:
#         post = Post.query.get(id)
#         if not post:
#             return jsonify({'message': 'Post not found'}), 404

#         db.session.delete(post)
#         db.session.commit()
#         return jsonify({'message': 'Post deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to delete post', 'error': str(e)}), 500



