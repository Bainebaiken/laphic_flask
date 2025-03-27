from functools import wraps
from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models import Provider  
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

# Define a Blueprint for providers-related routes
provider_bp = Blueprint('providers', __name__, url_prefix='/api/v1/providers')  # Adjusted Blueprint definition



# Admin required decorator
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Register a new provider
@provider_bp.route('/register', methods=['POST'])
def register_provider():
    try:
        data = request.get_json()
        new_provider = Provider(
            Name=data.get('Name'),
            Contact=data.get('Contact'),
            Email=data.get('Email'),
            Address=data.get('Address'),
            Password=data.get('Password')  # Ensure the password is hashed
        )
        db.session.add(new_provider)
        db.session.commit()
        return jsonify({'message': 'Provider registered successfully', 'Provider_ID': new_provider.Provider_ID}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register provider', 'details': str(e)}), 500
    

# Login endpoint
@provider_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('Email')
        password = data.get('Password')

        # Verify provider credentials
        provider = Provider.query.filter_by(Email=email).first()
        if not provider or not check_password_hash(provider.Password, password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Create access token
        access_token = create_access_token(
            identity={'Provider_ID': provider.Provider_ID, 'role': 'admin'},  # Adjust role logic as needed
            expires_delta=timedelta(hours=1)
        )
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to login', 'details': str(e)}), 500    

# Get all providers (Admin only)
@provider_bp.route('/', methods=['GET'])
@admin_required
def get_all_providers():
    try:
        providers = Provider.query.all()
        provider_list = [
            {
                'Provider_ID': p.Provider_ID,
                'Name': p.Name,
                'Contact': p.Contact,
                'Email': p.Email,
                'Address': p.Address
            } for p in providers
        ]
        return jsonify({'providers': provider_list}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve providers', 'details': str(e)}), 500

# Get a single provider
@provider_bp.route('/<int:provider_id>', methods=['GET'])
@jwt_required()
def get_provider(provider_id):
    try:
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        return jsonify({
            'Provider_ID': provider.Provider_ID,
            'Name': provider.Name,
            'Contact': provider.Contact,
            'Email': provider.Email,
            'Address': provider.Address
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve provider', 'details': str(e)}), 500

# Update provider information (Admin only)
@provider_bp.route('/<int:provider_id>', methods=['PUT'])
@admin_required
def update_provider(provider_id):
    try:
        data = request.get_json()
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404

        # Update fields
        provider.Name = data.get('Name', provider.Name)
        provider.Contact = data.get('Contact', provider.Contact)
        provider.Email = data.get('Email', provider.Email)
        provider.Address = data.get('Address', provider.Address)

        db.session.commit()
        return jsonify({'message': 'Provider updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update provider', 'details': str(e)}), 500

# Delete a provider (Admin only)
@provider_bp.route('/<int:provider_id>', methods=['DELETE'])
@admin_required
def delete_provider(provider_id):
    try:
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404

        db.session.delete(provider)
        db.session.commit()
        return jsonify({'message': 'Provider deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete provider', 'details': str(e)}), 500

# Get messages related to a provider
@provider_bp.route('/<int:provider_id>/messages', methods=['GET'])
@jwt_required()
def get_provider_messages(provider_id):
    try:
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404

        sent_messages = provider.messages_sent.all()
        received_messages = provider.messages_received.all()

        messages = {
            'sent_messages': [
                {
                    'Message_ID': m.Message_ID,
                    'Content': m.Content,
                    'Receiver_ID': m.Receiver_ID,
                    'Timestamp': m.Timestamp
                } for m in sent_messages
            ],
            'received_messages': [
                {
                    'Message_ID': m.Message_ID,
                    'Content': m.Content,
                    'Sender_ID': m.Sender_ID,
                    'Timestamp': m.Timestamp
                } for m in received_messages
            ]
        }
        return jsonify({'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve messages', 'details': str(e)}), 500

# # Admin required
# def admin_required(fn):
#     @wraps(fn)
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         user_info = get_jwt_identity()
#         if user_info['role'] != 'admin':
#             return jsonify({'error': 'Admin access required'}), 403
#         return fn(*args, **kwargs)
#     return wrapper

# # Create a new providers
# @provider_bp.route('/register', methods=['POST'])  
# def create_provider():
#     try:
#         data = request.get_json()
#         Provider_ID = data.get('Provider_ID')
#         Name = data.get('Name')
#         Contact = data.get('Contact')
#         messages_sent = data.get('messages_sent')
#         messages_received = data.get('messages_received')

#         new_provider = Provider(Provider_ID=Provider_ID, Name=Name, Contact=Contact,
#                         messages_sent=messages_sent, messages_received=messages_received)

#         db.session.add(new_provider)
#         db.session.commit()

#         return jsonify({'message': 'Post created successfully', 'id': new_provider.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create providers', 'error': str(e)}), 500



