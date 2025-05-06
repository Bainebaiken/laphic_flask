from flask import Blueprint, jsonify, request
from laphic_app.extensions import db
from laphic_app.models import Booking, Service
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime

# Define a Blueprint for booking-related routes
booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/booking')

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

# Create a new booking (Authenticated users)
@booking_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        required_fields = ['User_ID', 'Service_ID', 'Schedule_Date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: User_ID, Service_ID, Schedule_Date'}), 400

        # Ensure User_ID matches authenticated user (unless admin/superadmin)
        if data['User_ID'] != current_user['user_id'] and current_user['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Unauthorized to create booking for another user'}), 403

        # Validate Service_ID exists
        service = Service.query.get(data['Service_ID'])
        if not service:
            return jsonify({'error': 'Invalid Service_ID'}), 400

        # Parse Schedule_Date
        try:
            schedule_date = datetime.fromisoformat(data['Schedule_Date'])
        except ValueError:
            return jsonify({'error': 'Schedule_Date must be in ISO 8601 format (e.g., 2025-05-02T10:00:00)'}), 400

        new_booking = Booking(
            User_ID=data['User_ID'],
            Service_ID=data['Service_ID'],
            Booking_Date=datetime.utcnow(),
            Schedule_Date=schedule_date
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({
            'message': 'Booking created successfully',
            'booking': {
                'Booking_ID': new_booking.Booking_ID,
                'User_ID': new_booking.User_ID,
                'Service_ID': new_booking.Service_ID,
                'Booking_Date': new_booking.Booking_Date.isoformat(),
                'Schedule_Date': new_booking.Schedule_Date.isoformat(),
                'service': service.Name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create booking', 'details': str(e)}), 500

# Get all bookings (Admin/Superadmin only)
@booking_bp.route('/', methods=['GET'])
@admin_or_superadmin_required
def get_all_bookings():
    try:
        service_id = request.args.get('service_id', type=int)
        query = Booking.query
        if service_id:
            query = query.filter_by(Service_ID=service_id)
        
        bookings = query.all()
        booking_list = []
        for booking in bookings:
            service = Service.query.get(booking.Service_ID)
            booking_list.append({
                'Booking_ID': booking.Booking_ID,
                'User_ID': booking.User_ID,
                'Service_ID': booking.Service_ID,
                'Booking_Date': booking.Booking_Date.isoformat(),
                'Schedule_Date': booking.Schedule_Date.isoformat(),
                'service': service.Name if service else 'Unknown'
            })
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve bookings', 'details': str(e)}), 500

# Get bookings for a user (User or Admin/Superadmin)
@booking_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_bookings(user_id):
    try:
        current_user = get_jwt_identity()
        # Allow access if user_id matches JWT identity or user is admin/superadmin
        if current_user['user_id'] != user_id and current_user['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Unauthorized access to bookings'}), 403

        bookings = Booking.query.filter_by(User_ID=user_id).all()
        booking_list = []
        for booking in bookings:
            service = Service.query.get(booking.Service_ID)
            booking_list.append({
                'Booking_ID': booking.Booking_ID,
                'User_ID': booking.User_ID,
                'Service_ID': booking.Service_ID,
                'Booking_Date': booking.Booking_Date.isoformat(),
                'Schedule_Date': booking.Schedule_Date.isoformat(),
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

        # Allow access if User_ID matches JWT identity or user is admin/superadmin
        if booking.User_ID != current_user['user_id'] and current_user['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Unauthorized access to booking'}), 403

        service = Service.query.get(booking.Service_ID)
        return jsonify({
            'Booking_ID': booking.Booking_ID,
            'User_ID': booking.User_ID,
            'Service_ID': booking.Service_ID,
            'Booking_Date': booking.Booking_Date.isoformat(),
            'Schedule_Date': booking.Schedule_Date.isoformat(),
            'service': service.Name if service else 'Unknown'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve booking', 'details': str(e)}), 500

# Delete a booking by ID (Admin/Superadmin only)
@booking_bp.route('/<int:id>', methods=['DELETE'])
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