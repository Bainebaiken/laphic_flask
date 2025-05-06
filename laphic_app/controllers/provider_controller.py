from functools import wraps
from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models import Provider
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Define a Blueprint for providers-related routes
provider_bp = Blueprint('providers', __name__, url_prefix='/api/v1/providers')

# Superadmin required decorator
def superadmin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'superadmin':
            return jsonify({'error': 'Superadmin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Admin or Superadmin required decorator
def admin_or_superadmin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Admin or Superadmin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Register a new provider (public, creates regular provider with role 'admin')
@provider_bp.route('/register', methods=['POST'])
def register_provider():
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['Name', 'Contact', 'Email', 'Address', 'Password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if email already exists
        if Provider.query.filter_by(Email=data['Email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Create new provider with hashed password and default role 'admin'
        new_provider = Provider(
            Name=data['Name'],
            Contact=data['Contact'],
            Email=data['Email'],
            Address=data['Address'],
            Password=generate_password_hash(data['Password']),
            role='admin'  # Default role for regular provider registration
        )
        db.session.add(new_provider)
        db.session.commit()
        return jsonify({'message': 'Provider registered successfully', 'Provider_ID': new_provider.Provider_ID}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register provider', 'details': str(e)}), 500

# Create an admin provider (superadmin only)
@provider_bp.route('/create-admin', methods=['POST'])
@superadmin_required
def create_admin_provider():
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['Name', 'Contact', 'Email', 'Address', 'Password', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate role
        if data['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Invalid role. Must be admin or superadmin'}), 400

        # Check if email already exists
        if Provider.query.filter_by(Email=data['Email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Create new admin provider with hashed password
        new_provider = Provider(
            Name=data['Name'],
            Contact=data['Contact'],
            Email=data['Email'],
            Address=data['Address'],
            Password=generate_password_hash(data['Password']),
            role=data['role']
        )
        db.session.add(new_provider)
        db.session.commit()
        return jsonify({'message': 'Admin provider created successfully', 'Provider_ID': new_provider.Provider_ID}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create admin provider', 'details': str(e)}), 500

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

        # Create access token with provider's role
        access_token = create_access_token(
            identity={'Provider_ID': provider.Provider_ID, 'role': provider.role},
            expires_delta=timedelta(hours=1)
        )
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to login', 'details': str(e)}), 500

# Get all providers (Admin or Superadmin)
@provider_bp.route('/', methods=['GET'])
@admin_or_superadmin_required
def get_all_providers():
    try:
        providers = Provider.query.all()
        provider_list = [
            {
                'Provider_ID': p.Provider_ID,
                'Name': p.Name,
                'Contact': p.Contact,
                'Email': p.Email,
                'Address': p.Address,
                'role': p.role
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
            'Address': provider.Address,
            'role': provider.role
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve provider', 'details': str(e)}), 500

# Update provider information (Superadmin only)
@provider_bp.route('/<int:provider_id>', methods=['PUT'])
@superadmin_required
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
        if 'Password' in data:
            provider.Password = generate_password_hash(data['Password'])
        if 'role' in data and data['role'] in ['admin', 'superadmin']:
            provider.role = data['role']
        else:
            return jsonify({'error': 'Invalid role. Must be admin or superadmin'}), 400

        db.session.commit()
        return jsonify({'message': 'Provider updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update provider', 'details': str(e)}), 500

# Delete a provider (Superadmin only)
@provider_bp.route('/<int:provider_id>', methods=['DELETE'])
@superadmin_required
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

# Get messages related to a provider (Admin or Superadmin)
@provider_bp.route('/<int:provider_id>/messages', methods=['GET'])
@admin_or_superadmin_required
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
                    'Timestamp': m.Timestamp.isoformat()
                } for m in sent_messages
            ],
            'received_messages': [
                {
                    'Message_ID': m.Message_ID,
                    'Content': m.Content,
                    'Sender_ID': m.Sender_ID,
                    'Timestamp': m.Timestamp.isoformat()
                } for m in received_messages
            ]
        }
        return jsonify({'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve messages', 'details': str(e)}), 500