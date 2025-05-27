
from flask import Blueprint, jsonify, request
from laphic_app.extensions import db
from laphic_app.models import Booking, Service, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime
import re

# Define a Blueprint for booking-related routes
booking_bp = Blueprint('booking', __name__, url_prefix='/api/bookings')

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

# Validation function for booking data
def validate_booking_data(data):
    required_fields = ['name', 'phoneNumber', 'address', 'selectedServiceType', 
                      'selectedDate', 'selectedTime', 'distance', 'cost', 'paymentMethod']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f'Missing or empty field: {field}'
    
    # Validate phone number format
    phone_pattern = r'^\+?\d{9,15}$'
    if not re.match(phone_pattern, data['phoneNumber']):
        return False, 'Invalid phone number format'
    
    # Validate service type
    valid_services = [
        'Painting', 'Compound Design', 'Gypsum Work', 
        'Aluminum Works', 'furniture', 'Interior Design'
    ]
    if data['selectedServiceType'] not in valid_services:
        return False, 'Invalid service type'
    
    # Validate date format (YYYY-MM-DD)
    try:
        datetime.strptime(data['selectedDate'], '%Y-%m-%d')
    except ValueError:
        return False, 'Invalid date format. Use YYYY-MM-DD'
    
    # Validate time format (HH:MM AM/PM)
    try:
        datetime.strptime(data['selectedTime'], '%I:%M %p')
    except ValueError:
        return False, 'Invalid time format. Use HH:MM AM/PM'
    
    # Validate distance and cost
    if not isinstance(data['distance'], (int, float)) or data['distance'] <= 0:
        return False, 'Distance must be a positive number'
    if not isinstance(data['cost'], (int, float)) or data['cost'] <= 0:
        return False, 'Cost must be a positive number'
    
    # Validate payment method
    valid_payments = ['Mobile Money', 'Bank Transfer', 'Credit Card']
    if data['paymentMethod'] not in valid_payments:
        return False, 'Invalid payment method'
    
    return True, None

# Create a new booking (Authenticated users)
@booking_bp.route('/create', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data
        is_valid, error_message = validate_booking_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Verify user exists
        user = User.query.get(current_user['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify service exists
        service = Service.query.filter_by(Name=data['selectedServiceType']).first()
        if not service:
            return jsonify({'error': 'Invalid service type'}), 400
        
        # Create booking
        new_booking = Booking(
            user_id=current_user['user_id'],
            name=data['name'],
            phone_number=data['phoneNumber'],
            address=data['address'],
            service_type=data['selectedServiceType'],
            selected_date=data['selectedDate'],
            selected_time=data['selectedTime'],
            distance=data['distance'],
            cost=data['cost'],
            payment_method=data['paymentMethod'],
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': {
                'id': new_booking.id,
                'user_id': new_booking.user_id,
                'name': new_booking.name,
                'phone_number': new_booking.phone_number,
                'address': new_booking.address,
                'service_type': new_booking.service_type,
                'selected_date': new_booking.selected_date,
                'selected_time': new_booking.selected_time,
                'distance': new_booking.distance,
                'cost': new_booking.cost,
                'payment_method': new_booking.payment_method,
                'created_at': new_booking.created_at.isoformat(),
                'service': service.Name
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create booking', 'details': str(e)}), 500

# Get all bookings (Admin/Superadmin only)
@booking_bp.route('/all', methods=['GET'])
@admin_or_superadmin_required
def get_all_bookings():
    try:
        bookings = Booking.query.all()
        booking_list = []
        for booking in bookings:
            service = Service.query.filter_by(Name=booking.service_type).first()
            booking_list.append({
                'id': booking.id,
                'user_id': booking.user_id,
                'name': booking.name,
                'phone_number': booking.phone_number,
                'address': booking.address,
                'service_type': booking.service_type,
                'selected_date': booking.selected_date,
                'selected_time': booking.selected_time,
                'distance': booking.distance,
                'cost': booking.cost,
                'payment_method': booking.payment_method,
                'created_at': booking.created_at.isoformat(),
                'service': service.Name if service else 'Unknown'
            })
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve bookings', 'details': str(e)}), 500

# Get bookings for a user (User or Admin/Superadmin)
@booking_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_bookings(user_id):
    try:
        current_user = get_jwt_identity()
        # Allow access if user_id matches JWT identity or user is admin/superadmin
        if current_user['user_id'] != user_id and current_user['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Unauthorized access to bookings'}), 403

        bookings = Booking.query.filter_by(user_id=user_id).all()
        booking_list = []
        for booking in bookings:
            service = Service.query.filter_by(Name=booking.service_type).first()
            booking_list.append({
                'id': booking.id,
                'user_id': booking.user_id,
                'name': booking.name,
                'phone_number': booking.phone_number,
                'address': booking.address,
                'service_type': booking.service_type,
                'selected_date': booking.selected_date,
                'selected_time': booking.selected_time,
                'distance': booking.distance,
                'cost': booking.cost,
                'payment_method': booking.payment_method,
                'created_at': booking.created_at.isoformat(),
                'service': service.Name if service else 'Unknown'
            })
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user bookings', 'details': str(e)}), 500

# Get a single booking by ID (User or Admin/Superadmin)
@booking_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_booking(id):
    try:
        current_user = get_jwt_identity()
        booking = Booking.query.get(id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Allow access if user_id matches JWT identity or user is admin/superadmin
        if booking.user_id != current_user['user_id'] and current_user['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Unauthorized access to booking'}), 403

        service = Service.query.filter_by(Name=booking.service_type).first()
        return jsonify({
            'id': booking.id,
            'user_id': booking.user_id,
            'name': booking.name,
            'phone_number': booking.phone_number,
            'address': booking.address,
            'service_type': booking.service_type,
            'selected_date': booking.selected_date,
            'selected_time': booking.selected_time,
            'distance': booking.distance,
            'cost': booking.cost,
            'payment_method': booking.payment_method,
            'created_at': booking.created_at.isoformat(),
            'service': service.Name if service else 'Unknown'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve booking', 'details': str(e)}), 500

# Delete a booking by ID (Admin/Superadmin only)
@booking_bp.route('/delete/<int:id>', methods=['DELETE'])
@admin_or_superadmin_required
def delete_booking(id):
    try:
        booking = Booking.query.get(id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete booking', 'details': str(e)}), 500