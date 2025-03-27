from flask import Blueprint, jsonify, request
from . import db  
from laphic_app.models.Booking import Booking  
from flask_jwt_extended import jwt_required
from functools import wraps
# Define a Blueprint for booking-related routes
booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/booking')



# Create a new booking
@booking_bp.route('/register', methods=['POST'])
def create_article():
    data = request.get_json()
    Booking_ID = data.get('Booking_ID')
    User_ID = data.get('User_ID')
    Service_ID = data.get('Service_ID')
    Booking_Date = data.get('Booking_Date')  # Optional field
    Schedule_Date =data.get('Schedule_Date')


    service = data.get('Service_ID')

    if service == "Painting":
        Service_ID = 1
    elif service == "Reinnovation":
        Service_ID = 2
    elif service == "Gypsum work":
        Service_ID = 3
    elif service == "Compound_designing":
        Service_ID = 5
    elif service == "interior_design":
        Service_ID = 4
    else:
        Service_ID = 1

    new_book = Booking( Booking_ID=Booking_ID,User_ID=User_ID, Service_ID=Service_ID, Booking_Date=Booking_Date, Schedule_Date=Schedule_Date)

    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Booking created successfully', 'id': new_book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create booking', 'error': str(e)}), 500

# Get all booking
@booking_bp.route('/booking', methods=['GET'])
def get_all_articles():
    try:
        booking = Booking.query.all() # .filter(Service_ID=1)
        booking_list = []
        for booking in booking:
            if booking.Service_ID == 1:
                service = "Painting"
            elif booking.Service_ID == 2:
                service = "Reinnovation"
            elif booking.Service_ID == 3: 
                service = "Gypsum work"
            elif service == 5:
                Service_ID = "Compound_designing"
            elif service == 4:
                Service_ID = "interior_design"
            else:
                service = "Reinnovation"

            booking_list.append({
                'id': booking.id,
                'Booking_ID':booking.Booking_ID,
                'User_ID': booking.User_ID,
                'Service_ID': booking.Service_ID,
                'Booking_Date': booking.Booking_Date,
                'Schedule_Date' :booking.Schedule_Date,
                'date' :booking.date,
                'service': service
            })
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve booking', 'error': str(e)}), 500



# Get sports booking
@booking_bp.route('/get_Painting', methods=['GET'])
def get_painting_booking():
    try:
        booking = Booking.query.all()
        booking_list = []
        for booking in booking:
            service = "Painting"
            if booking.Service_ID == 1:
                booking_list.append({
                    'id': booking.id,
                    'Booking_ID':booking.Booking_ID,
                    'User_ID': booking.User_ID,
                    'Service_ID': booking.Service_ID,
                    'Booking_Date': booking.Booking_Date,
                    'Schedule_Date' :booking.Schedule_Date,
                    'date' :booking.date,
                    'service': service
                })
        print(len(booking_list))
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve booking', 'error': str(e)}), 500



# Get politics booking
@booking_bp.route('/get_compound_designing', methods=['GET'])
def get_compound_designing_booking():
    try:
        booking = Booking.query.all()
        booking_list = []
        for booking in booking:
            service = "Compound_designing"
            if booking.Service_ID == 5:
                booking_list.append({
                    'id': booking.id,
                    'Booking_ID':booking.Booking_ID,
                    'User_ID': booking.User_ID,
                    'Service_ID': booking.Service_ID,
                    'Booking_Date': booking.Booking_Date,
                    'Schedule_Date' :booking.Schedule_Date,
                    'date' :booking.date,
                    'service': service
                })
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve booking', 'error': str(e)}), 500
    


# Get interior booking
@booking_bp.route('/get_interior_design', methods=['GET'])
def get_interior_design_booking():
    try:
        booking = Booking.query.all()
        booking_list = []
        for booking in booking:
            service = "interior_design"
            if booking.Service_ID == 4:
                booking_list.append({
                    'id': booking.id,
                    'Booking_ID':booking.Booking_ID,
                    'User_ID': booking.User_ID,
                    'Service_ID': booking.Service_ID,
                    'Booking_Date': booking.Booking_Date,
                    'Schedule_Date' :booking.Schedule_Date,
                    'date' :booking.date,
                    'service': service
                })
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve booking', 'error': str(e)}), 500


# Get a single booking by ID
@booking_bp.route('/<int:id>', methods=['GET'])
def get_booking(id):
    try:
        booking = Booking.query.get(id)
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404

        return jsonify({
            'id': booking.id,
            'Booking_ID':booking.Booking_ID,
            'User_ID': booking.User_ID,
            'Service_ID': booking.Service_ID,
            'Booking_Date': booking.Booking_Date,
            'Schedule_Date' :booking.Schedule_Date,
            'date' :booking.date
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve booking', 'error': str(e)}), 500





# Delete an booking by ID
@booking_bp.route('/delete_booking', methods=['DELETE'])
# @admin_required
def delete_booking():
    try:
        
        data = request.get_json()

        email = data.get('email')
        print(email)
        id = data.get('id')
        print(id)

        booking = Booking.query.get(id)

        if not booking:
            return jsonify({'message': 'Booking not found'}), 404

        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete booking', 'error': str(e)}), 500
