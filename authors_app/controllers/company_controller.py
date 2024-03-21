from flask import Blueprint, request, jsonify
from datetime import datetime
from authors_app.controllers import company_controller
from authors_app import db


company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
def register_company():
    try:
        # Extracting request data
        id = request.json.get('id')
        name= request.json.get('name')
        origin= request.json.get('origin')
        description= request.json.get('description')
        created_at = request.json.get('created_at')
        updated_at = request.json.get('updated_at')
     
        
        # Basic input validation
        if not id:
            return jsonify({"error": 'Your company ID is required'})

        if not name:
            return jsonify({"error": 'Your company name is required'})

        if not origin:
            return jsonify({"error": 'Your company origin is required'})

        if not description:
            return jsonify({"error": 'Please add a description of your company'})

        # Creating a new user (assuming you have a valid User model)
        user = company(
            first_name='first_name',
            last_name='last_name',
            email='email',
            contact='contact',
            image='image',
            password='password',
            biography='biography',
            user_type='user_type'
        )

        db.session.add(user)
        db.session.commit()

        # Building a response message
        message = f"company {user.first_name} {user.last_name} company has been created"
        return jsonify({"message": message}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500