from flask import Blueprint, jsonify, request
from datetime import datetime
from laphic_app.extensions import db
from functools import wraps
from flask_jwt_extended import jwt_required
from laphic_app.models import  service


# # Define a Blueprint for service-related routes
service_bp = Blueprint('service', __name__, url_prefix='/api/v1/services')
# Routes for CRUD operations

# Create a new service
@service_bp.route('/register', methods=['POST'])
def create_service():
    data = request.get_json()
    new_service = service.Service(
        Name=data['Name'],
        Category=data['Category'],
        Description=data.get('Description'),
        Cost=data['Cost']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service created successfully!", "service": data}), 201

# Get all services
@service_bp.route('/services', methods=['GET'])
def get_services():
    services = service.Service.query.all()
    return jsonify([{
        "Service_ID": service.Service_ID,
        "Name": service.Name,
        "Category": service.Category,
        "Description": service.Description,
        "Cost": service.Cost
    } for service in services]), 200

# Get a single service by ID
@service_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = service.Service.query.get_or_404(service_id)
    return jsonify({
        "Service_ID": service.Service_ID,
        "Name": service.Name,
        "Category": service.Category,
        "Description": service.Description,
        "Cost": service.Cost
    }), 200

# Update a service by ID
@service_bp.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    data = request.get_json()
    service = service.Service.query.get_or_404(service_id)

    service.Name = data.get('Name', service.Name)
    service.Category = data.get('Category', service.Category)
    service.Description = data.get('Description', service.Description)
    service.Cost = data.get('Cost', service.Cost)

    db.session.commit()
    return jsonify({"message": "Service updated successfully!"}), 200

# Delete a service by ID
@service_bp.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = service.Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully!"}), 200

# @service_bp.route('/create_service', methods=['POST'])
# def create_service():
#     print(1)
#     data = request.get_json()
#     print(data)
#     Service_ID = data.get('Service_ID')
#     print(Service_ID)
#     Name = data.get('Name')
#     print(Name)
#     Category = data.get('Category')
#     Description = data.get('Description')
#     Cost = data.get('Cost')
   
   
    
#     new_service = service(Service_ID=Service_ID, Name=Name, Category=Category,Description=Description,Cost=Cost)

#     try:
#         db.session.add(new_service)
#         db.session.commit()
#         return jsonify({'message': ' service created successfully', 'id': new_service.id}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create  service', 'error': str(e)}), 500






