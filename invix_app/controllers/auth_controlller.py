from flask import Blueprint, request, jsonify
from invix_app.models.user import User
from invix_app.extensions import db, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from invix_app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR
from flask_jwt_extended import create_access_token
from http import HTTPStatus
# auth Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        # Storing variables
        first_name = data['firstname']
        last_name = data['lastname']
        email = data['email']
        contact = data['contact']
        user_type = data['usertype']
        image = data['image']  
        password = data['password']
        biography = data['biography']

        # Checking for null validations and constraints
        if not first_name:
            return jsonify({'error': "Your first_name is required"}), 400
        if not last_name:
            return jsonify({'error': "Your last_name is required"}), 400
        if not email:
            return jsonify({'error': "Your email is required"}), 400
        if not contact:
            return jsonify({'error': "Your contact is required"}), 400
        if not user_type:
            return jsonify({'error': "Your user_type is required"}), 400
        if not image:
            return jsonify({'error': "Your image is required"}), 400
        if len(password) < 8:
            return jsonify({'error': "Your password is too short"}), 400

        # Checking if the email or contact already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': "Email already exists"}), 400
        if User.query.filter_by(contact=contact).first():
            return jsonify({'error': "Contact already exists"}), 400
    

        # Hashing the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Creating a new user
        new_user = User(first_name=first_name, last_name=last_name, password=hashed_password, email=email,
                        contact=contact, user_type=user_type, image=image, biography=biography)
        db.session.add(new_user)
        db.session.commit()

        # Returning success response
        return jsonify({
            'message': f'{new_user.get_full_name()} has been successfully created as a {new_user.user_type}',
            'user': {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "contact": new_user.contact,
                "image": image,
                "User-type": new_user.user_type,
                "biography": new_user.biography,
                "created_at": new_user.created_at
            }
        }), 201

    except KeyError as e:
        # Handle the case where a required field is missing in the request body
        return jsonify({'error': f'Missing {e.args[0]} in request body'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500




@auth_bp.route('/login', methods=['POST'])
def login():
    print(1)
    try:
        print(2)
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({'message': 'JSON data not found in request'}), HTTPStatus.BAD_REQUEST
        
        email = data.get('email')
        password = data.get('password')
        
        print(email)
        print(password)

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), HTTPStatus.BAD_REQUEST
        
        user = User.query.filter_by(email=email).first()
        
        print(user)
        
        if user:
            is_correct_password = bcrypt.check_password_hash(user.password, password)
            print(is_correct_password)
            if is_correct_password:
                access_token = create_access_token(identity=user.id)
                print(access_token)
                return jsonify({
                    'user': {
                        'id': user.id,
                        'user_name': user.get_full_name(),  # Adjust based on your User model
                        'email': user.email,
                        'access_token': access_token
                    }
                }), HTTPStatus.OK
            else:
                print(11)
                return jsonify({'message': 'Invalid password'}), HTTPStatus.UNAUTHORIZED
        else:
            print(22)
            return jsonify({'message': 'Invalid email address'}), HTTPStatus.UNAUTHORIZED
        
    except Exception as e:
        print(3)
        print(str(e))  # Print the error for debugging purposes
        return jsonify({
            'error': 'Internal Server Error'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

# Define the endpoint for a specific user
@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
        
        # Return user details
        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact': user.contact,
            'user_type': user.user_type,
            'biography': user.biography,
            'image': user.image,
            'created_at': user.created_at
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Define the endpoint to get all users
@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'contact': user.contact,
                'user_type': user.user_type,
                'biography': user.biography,
                'image': user.image,
                'created_at': user.created_at
            }
            user_list.append(user_data)
        
        # Return the list of users
        return jsonify({'users': user_list}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Define the endpoint to delete a user
@auth_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Define the edit user endpoint
@auth_bp.route('/edit/<int:user_id>', methods=["PUT"])
@jwt_required()
def edit_user(user_id):
    try:
        data = request.json
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            new_email = data['email']
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'The email already exists'}), HTTP_409_CONFLICT
            user.email = new_email
        if 'image' in data:
            user.image = data['image']
        if 'biography' in data:
            user.biography = data['biography']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'password' in data:
            password = data['password']
            if len(password) < 8:
                return jsonify({'error': 'Password must have at least 8 characters'}), HTTP_400_BAD_REQUEST
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if 'contact' in data:
            user.contact = data['contact']

        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR    
