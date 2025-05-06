from flask import Blueprint, jsonify, request
from laphic_app.extensions import db
from laphic_app.models import Service
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define a Blueprint for service-related routes
service_bp = Blueprint('service', __name__, url_prefix='/api/v1/services')

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

# Create a new service (Admin or Superadmin only)
@service_bp.route('/', methods=['POST'])
@admin_or_superadmin_required
def create_service():
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['Name', 'Category', 'Cost']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: Name, Category, Cost'}), 400

        # Validate Cost is a number
        if not isinstance(data['Cost'], (int, float)) or data['Cost'] < 0:
            return jsonify({'error': 'Cost must be a non-negative number'}), 400

        new_service = Service(
            Name=data['Name'],
            Category=data['Category'],
            Description=data.get('Description', ''),
            Cost=data['Cost']
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({
            'message': 'Service created successfully',
            'service': {
                'Service_ID': new_service.Service_ID,
                'Name': new_service.Name,
                'Category': new_service.Category,
                'Description': new_service.Description,
                'Cost': new_service.Cost
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create service', 'details': str(e)}), 500

# Get all services (Public access)
@service_bp.route('/', methods=['GET'])
def get_services():
    try:
        services = Service.query.all()
        return jsonify([{
            'Service_ID': service.Service_ID,
            'Name': service.Name,
            'Category': service.Category,
            'Description': service.Description,
            'Cost': service.Cost
        } for service in services]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve services', 'details': str(e)}), 500

# Get a single service by ID (Public access)
@service_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        return jsonify({
            'Service_ID': service.Service_ID,
            'Name': service.Name,
            'Category': service.Category,
            'Description': service.Description,
            'Cost': service.Cost
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve service', 'details': str(e)}), 500

# Update a service by ID (Admin or Superadmin only)
@service_bp.route('/<int:service_id>', methods=['PUT'])
@admin_or_superadmin_required
def update_service(service_id):
    try:
        data = request.get_json()
        service = Service.query.get_or_404(service_id)

        # Validate Cost if provided
        if 'Cost' in data and (not isinstance(data['Cost'], (int, float)) or data['Cost'] < 0):
            return jsonify({'error': 'Cost must be a non-negative number'}), 400

        service.Name = data.get('Name', service.Name)
        service.Category = data.get('Category', service.Category)
        service.Description = data.get('Description', service.Description)
        service.Cost = data.get('Cost', service.Cost)

        db.session.commit()
        return jsonify({'message': 'Service updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update service', 'details': str(e)}), 500

# Delete a service by ID (Admin or Superadmin only)
@service_bp.route('/<int:service_id>', methods=['DELETE'])
@admin_or_superadmin_required
def delete_service(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete service', 'details': str(e)}), 500