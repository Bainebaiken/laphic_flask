from flask import Blueprint, request, jsonify
from datetime import datetime
from authors_app.extensions import db
from authors_app.models.books import Books 
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager

book = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book.route('/register', methods=['POST'])
def register_book():
    try:
        # Extracting request data
        id = request.json.get('id')
        title=request.json.get('title')
        description=request.json.get('description')
        price=request.json.get('price')
        image=request.json.get('image')
        pages= request.json.get('pages')
        company_id= request.json.get('company _id ')
        user_id=request.json.get('user_id')
        created_at=request.json.get('created_at')
        updated_at=request.json.get('updated_at')

        # Basic input validation
        if not id:
            return jsonify({"error": 'Your book ID is required'})

        if not title:
            return jsonify({"error": 'Your book title is required'})

        if not description:
            return jsonify({"error": 'The description is required'})

        if not price:
            return jsonify({"error": 'The price is required'})

        if not image:
            return jsonify({"error": 'The image is required'})
        
        if not pages:
            return jsonify({"error": 'The page is required'})
        if not company_id:
            return jsonify({"error": 'The company_id is required'})

        if not user_id:
            return jsonify({"error": 'Please specify the user_id'})

        # Creating a new book
        new_book = Books(
            id=id,
            title=title,
            description=description,
            price=price,
            image=image,
            pages=pages,
            company_id=company_id,
            user_id=user_id,
            created_at=created_at,
            updated_at=updated_at
        )

        # Adding and committing to the database
        db.session.add(new_book)
        db.session.commit()

        # Building a response message
        return jsonify({"message": f"Book '{new_book.title}', ID '{new_book.id}' has been uploaded"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})
    
@book.route("/<int:id>") 
@jwt_required()
def get_book(id):
    try:
        current_user = get_jwt_identity()  # Get current user using get_jwt_identity
        book = Books.query.filter_by(user_id=current_user, id=id).first()

        if not book:
            return jsonify({'error': 'Item not found'}), 404
        
        # Return book details
        return jsonify({
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'price': book.price,
            'image': book.image,
            'pages': book.pages,
            'company_id': book.company_id,
            'user_id': book.user_id
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    