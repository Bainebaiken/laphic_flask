from flask import Blueprint, jsonify, request
from datetime import datetime
from invix_app.extensions import db
from functools import wraps
from flask_jwt_extended import jwt_required
from invix_app.models.category import  Category


# # Define a Blueprint for category-related routes
category_bp = Blueprint('category', __name__, url_prefix='/api/v1/categories')
# Routes for CRUD operations

@category_bp.route('/create_category', methods=['POST'])
def create_category():
    print(1)
    data = request.get_json()
    print(data)
    name = data.get('name')
    print(name)
    slug = data.get('slug')
    print(slug)
    
    new_category = Category(name=name, slug=slug)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': ' category created successfully', 'id': new_category.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create  category', 'error': str(e)}), 500






# @category_bp.route('/business', methods=['POST'])
# def create_business_category():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')  # Optional field

#     new_category = Category(name=name, slug=slug, content_id=content_id)

#     try:
#         db.session.add(new_category)
#         db.session.commit()
#         return jsonify({'message': 'Business category created successfully', 'id': new_category.id}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create business category', 'error': str(e)}), 500


# @category_bp.route('/education', methods=['POST'])
# def create_education_category():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')  # Optional field

#     new_category = Category(name=name, slug=slug, content_id=content_id)

#     try:
#         db.session.add(new_category)
#         db.session.commit()
#         return jsonify({'message': 'Education category created successfully', 'id': new_category.id}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create education category', 'error': str(e)}), 500


# @category_bp.route('/politics', methods=['POST'])
# def create_politics_category():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')  # Optional field

#     new_category = Category(name=name, slug=slug, content_id=content_id)

#     try:
#         db.session.add(new_category)
#         db.session.commit()
#         return jsonify({'message': 'Politics category created successfully', 'id': new_category.id}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create politics category', 'error': str(e)}), 500


# @category_bp.route('/general', methods=['GET'])
# def get_general_articles():
#     try:
#         articles = Article.query.all()
#         article_list = []
#         for article in articles:
#             article_list.append({
#                 'id': article.id,
#                 'text': article.text,
#                 'video': article.video,
#                 'image': article.image,
#                 'category': article.category.name  # Assuming a relationship exists
#             })
#         return jsonify(article_list), 200
#     except Exception as e:
#         return jsonify({'message': 'Failed to retrieve articles', 'error': str(e)}), 500

# Sports_bp = Blueprint('sports', __name__)


# @Sports_bp.route('/sports', methods=['POST'])
# def create_sports():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')

#     if not name or not slug:
#         return jsonify({"error": "Missing required fields"}), 400

#     new_sports = Sports(name=name, slug=slug, content_id=content_id)
#     db.session.add(new_sports)
#     db.session.commit()

#     return jsonify({
#         'id': new_sports.id,
#         'name': new_sports.name,
#         'slug': new_sports.slug,
#         'content_id': new_sports.content_id
#     }), 201

# @Sports_bp.route('/sports/<int:id>', methods=['GET'])
# def get_sports(id):
#     sports = Sports.query.get_or_404(id)
#     return jsonify({
#         'id': sports.id,
#         'name': sports.name,
#         'slug': sports.slug,
#         'content_id': sports.content_id
#     }), 200

# @Sports_bp.route('/sports', methods=['GET'])
# def get_all_sports():
#     sports_list = Sports.query.all()
#     return jsonify([{
#         'id': sports.id,
#         'name': sports.name,
#         'slug': sports.slug,
#         'content_id': sports.content_id
#     } for sports in sports_list]), 200

# @Sports_bp.route('/sports/<int:id>', methods=['PUT'])
# def update_sports(id):
#     data = request.get_json()
#     sports = Sports.query.get_or_404(id)

#     sports.name = data.get('name', sports.name)
#     sports.slug = data.get('slug', sports.slug)
#     sports.content_id = data.get('content_id', sports.content_id)

#     db.session.commit()

#     return jsonify({
#         'id': sports.id,
#         'name': sports.name,
#         'slug': sports.slug,
#         'content_id': sports.content_id
#     }), 200

# @Sports_bp.route('/sports/<int:id>', methods=['DELETE'])
# @admin_required
# def delete_sports(id):
#     sports = Sports.query.get_or_404(id)
#     db.session.delete(sports)
#     db.session.commit()
    
#     return jsonify({"message": "Deleted"}), 204

# def register_blueprints(app):
#     app.register_blueprint(Sports_bp, url_prefix='/api')    


# Business_bp = Blueprint('business', __name__)



# @Business_bp.route('/business', methods=['POST'])

# def create_business():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')

#     if not name or not slug:
#         return jsonify({"error": "Missing required fields"}), 400

#     new_business = Business(name=name, slug=slug, content_id=content_id)
#     db.session.add(new_business)
#     db.session.commit()

#     return jsonify({
#         'id': new_business.id,
#         'name': new_business.name,
#         'slug': new_business.slug,
#         'content_id': new_business.content_id
#     }), 201

# @Business_bp.route('/business/<int:id>', methods=['GET'])
# def get_business(id):
#     business = Business.query.get_or_404(id)
#     return jsonify({
#         'id': business.id,
#         'name': business.name,
#         'slug': business.slug,
#         'content_id': business.content_id
#     }), 200

# @Business_bp.route('/business', methods=['GET'])
# def get_all_businesses():
#     businesses = Business.query.all()
#     return jsonify([{
#         'id': business.id,
#         'name': business.name,
#         'slug': business.slug,
#         'content_id': business.content_id
#     } for business in businesses]), 200

# @Business_bp.route('/business/<int:id>', methods=['PUT'])
# def update_business(id):
#     data = request.get_json()
#     business = Business.query.get_or_404(id)

#     business.name = data.get('name', business.name)
#     business.slug = data.get('slug', business.slug)
#     business.content_id = data.get('content_id', business.content_id)

#     db.session.commit()

#     return jsonify({
#         'id': business.id,
#         'name': business.name,
#         'slug': business.slug,
#         'content_id': business.content_id
#     }), 200

# @Business_bp.route('/business/<int:id>', methods=['DELETE'])
# @admin_required
# def delete_business(id):
#     business = Business.query.get_or_404(id)
#     db.session.delete(business)
#     db.session.commit()
    
#     return jsonify({"message": "Deleted"}), 204

# def register_blueprints(app):
#     app.register_blueprint(Business_bp, url_prefix='/api')   




# Education_bp = Blueprint('education', __name__)



# @Education_bp.route('/education', methods=['POST'])
# def create_education():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')

#     if not name or not slug:
#         return jsonify({"error": "Missing required fields"}), 400

#     new_education = Education(name=name, slug=slug, content_id=content_id)
#     db.session.add(new_education)
#     db.session.commit()

#     return jsonify({
#         'id': new_education.id,
#         'name': new_education.name,
#         'slug': new_education.slug,
#         'content_id': new_education.content_id
#     }), 201

# @Education_bp.route('/education/<int:id>', methods=['GET'])
# def get_education(id):
#     education = Education.query.get_or_404(id)
#     return jsonify({
#         'id': education.id,
#         'name': education.name,
#         'slug': education.slug,
#         'content_id': education.content_id
#     }), 200

# @Education_bp.route('/education', methods=['GET'])
# def get_all_education():
#     education_list = Education.query.all()
#     return jsonify([{
#         'id': education.id,
#         'name': education.name,
#         'slug': education.slug,
#         'content_id': education.content_id
#     } for education in education_list]), 200

# @Education_bp.route('/education/<int:id>', methods=['PUT'])
# def update_education(id):
#     data = request.get_json()
#     education = Education.query.get_or_404(id)

#     education.name = data.get('name', education.name)
#     education.slug = data.get('slug', education.slug)
#     education.content_id = data.get('content_id', education.content_id)

#     db.session.commit()

#     return jsonify({
#         'id': education.id,
#         'name': education.name,
#         'slug': education.slug,
#         'content_id': education.content_id
#     }), 200

# @Education_bp.route('/education/<int:id>', methods=['DELETE'])
# @admin_required
# def delete_education(id):
#     education = Education.query.get_or_404(id)
#     db.session.delete(education)
#     db.session.commit()
    
#     return jsonify({"message": "Deleted"}), 204

# def register_blueprints(app):
#     app.register_blueprint(Education_bp, url_prefix='/api')   



# Adverts_bp = Blueprint('adverts', __name__)



# @Adverts_bp.route('/adverts', methods=['POST'])
# def create_adverts():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')

#     if not name or not slug:
#         return jsonify({"error": "Missing required fields"}), 400

#     new_adverts = Adverts(name=name, slug=slug, content_id=content_id)
#     db.session.add(new_adverts)
#     db.session.commit()

#     return jsonify({
#         'id': new_adverts.id,
#         'name': new_adverts.name,
#         'slug': new_adverts.slug,
#         'content_id': new_adverts.content_id
#     }), 201

# @Adverts_bp.route('/adverts/<int:id>', methods=['GET'])
# def get_adverts(id):
#     adverts = Adverts.query.get_or_404(id)
#     return jsonify({
#         'id': adverts.id,
#         'name': adverts.name,
#         'slug': adverts.slug,
#         'content_id': adverts.content_id
#     }), 200

# @Adverts_bp.route('/adverts', methods=['GET'])
# def get_all_adverts():
#     adverts_list = Adverts.query.all()
#     return jsonify([{
#         'id': adverts.id,
#         'name': adverts.name,
#         'slug': adverts.slug,
#         'content_id': adverts.content_id
#     } for adverts in adverts_list]), 200

# @Adverts_bp.route('/adverts/<int:id>', methods=['PUT'])
# def update_adverts(id):
#     data = request.get_json()
#     adverts = Adverts.query.get_or_404(id)

#     adverts.name = data.get('name', adverts.name)
#     adverts.slug = data.get('slug', adverts.slug)
#     adverts.content_id = data.get('content_id', adverts.content_id)

#     db.session.commit()

#     return jsonify({
#         'id': adverts.id,
#         'name': adverts.name,
#         'slug': adverts.slug,
#         'content_id': adverts.content_id
#     }), 200

# @Adverts_bp.route('/adverts/<int:id>', methods=['DELETE'])
# @admin_required
# def delete_adverts(id):
#     adverts = Adverts.query.get_or_404(id)
#     db.session.delete(adverts)
#     db.session.commit()
    
#     return jsonify({"message": "Deleted"}), 204

# def register_blueprints(app):
#     app.register_blueprint(Adverts_bp, url_prefix='/api')        


# General_bp = Blueprint('general', __name__)


# @General_bp.route('/general', methods=['POST'])
# def create_general():
#     data = request.get_json()
#     name = data.get('name')
#     slug = data.get('slug')
#     content_id = data.get('content_id')

#     if not name or not slug:
#         return jsonify({"error": "Missing required fields"}), 400

#     new_general = General(name=name, slug=slug, content_id=content_id)
#     db.session.add(new_general)
#     db.session.commit()

#     return jsonify({
#         'id': new_general.id,
#         'name': new_general.name,
#         'slug': new_general.slug,
#         'content_id': new_general.content_id
#     }), 201

# @General_bp.route('/general/<int:id>', methods=['GET'])
# def get_general(id):
#     general = General.query.get_or_404(id)
#     return jsonify({
#         'id': general.id,
#         'name': general.name,
#         'slug': general.slug,
#         'content_id': general.content_id
#     }), 200

# @General_bp.route('/general', methods=['GET'])
# def get_all_general():
#     general_list = General.query.all()
#     return jsonify([{
#         'id': general.id,
#         'name': general.name,
#         'slug': general.slug,
#         'content_id': general.content_id
#     } for general in general_list]), 200

# @General_bp.route('/general/<int:id>', methods=['PUT'])
# def update_general(id):
#     data = request.get_json()
#     general = General.query.get_or_404(id)

#     general.name = data.get('name', general.name)
#     general.slug = data.get('slug', general.slug)
#     general.content_id = data.get('content_id', general.content_id)

#     db.session.commit()

#     return jsonify({
#         'id': general.id,
#         'name': general.name,
#         'slug': general.slug,
#         'content_id': general.content_id
#     }), 200

# @General_bp.route('/general/<int:id>', methods=['DELETE'])
# @admin_required
# def delete_general(id):
#     general = General.query.get_or_404(id)
#     db.session.delete(general)
#     db.session.commit()
    
#     return jsonify({"message": "Deleted"}), 204

# def register_blueprints(app):
#     app.register_blueprint(General_bp, url_prefix='/api')    