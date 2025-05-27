# from flask import Blueprint, request, jsonify
# from laphic_app.extensions import db, bcrypt, jwt
# from laphic_app.models.user import User
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from flask_cors import CORS  # Add this
# import re
# from sqlalchemy.exc import SQLAlchemyError

# auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")
# CORS(auth_bp, resources={r"/auth/*": {"origins": ["http://localhost:*"]}})  # Allow all localhost ports

# @auth_bp.route("/register", methods=["POST"])
# def register():
#     try:
#         data = request.get_json()
#         print(f"Received request from {request.origin}: {data}")  # Enhanced debug log
#         if not data:
#             return jsonify({"error": "No data provided", "message": None}), 400

#         required_fields = ["name", "email", "phone", "password"]
#         if not all(field in data and data[field] for field in required_fields):
#             return jsonify({"error": "All required fields (name, email, phone, password) must be filled", "message": None}), 400

#         if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
#             return jsonify({"error": "Invalid email format", "message": None}), 400
#         if not re.match(r"^\+?1?\d{9,15}$", data["phone"]):
#             return jsonify({"error": "Invalid phone number format", "message": None}), 400
#         if len(data["password"]) < 8:
#             return jsonify({"error": "Password must be at least 8 characters", "message": None}), 400

#         if User.query.filter_by(email=data["email"].lower()).first():
#             return jsonify({"error": "Email is already registered", "message": None}), 400

#         user_type = data.get("user_type", "user")
#         allowed_types = ["user", "customer", "admin", "super_admin"]
#         if user_type not in allowed_types:
#             return jsonify({"error": "Invalid user type", "message": None}), 400
#         if user_type in ["admin", "super_admin"]:
#             return jsonify({"error": "Cannot register as admin or super_admin through public endpoint", "message": None}), 403

#         hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

#         new_user = User(
#             name=data["name"],
#             email=data["email"].lower(),
#             phone=data["phone"],
#             password_hash=hashed_password,
#             user_type=user_type
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({"message": "User registered successfully", "user": new_user.to_dict(), "error": None}), 201

#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

# @auth_bp.route("/login", methods=["POST"])
# def login():
#     try:
#         data = request.get_json()
#         print(f"Received data: {data}")
#         if not data:
#             print("No data provided")
#             return jsonify({"error": "No data provided", "message": None}), 400

#         email = data.get("email", "").strip().lower()
#         password = data.get("password", "").strip()
#         print(f"Email: {email}, Password: {'*' * len(password)}")

#         if not email or not password:
#             print("Email or password missing")
#             return jsonify({"error": "Email and password are required", "message": None}), 400

#         user = User.query.filter_by(email=email).first()
#         print(f"User found: {user}")
#         if not user:
#             print("User not found")
#             return jsonify({"error": "Invalid email or password", "message": None}), 401

#         if not bcrypt.check_password_hash(user.password_hash, password):
#             print("Password mismatch")
#             return jsonify({"error": "Invalid email or password", "message": None}), 401

#         access_token = create_access_token(identity={"user_id": user.user_id, "user_type": user.user_type})
#         print(f"Token generated: {access_token}")
#         return jsonify({
#             "message": "Login successful",
#             "token": access_token,
#             "user": user.to_dict(),
#             "error": None
#         }), 200

#     except ValueError as ve:
#         print(f"ValueError: {str(ve)}")
#         return jsonify({"error": f"Invalid input: {str(ve)}", "message": None}), 400
#     except SQLAlchemyError as se:
#         print(f"SQLAlchemyError: {str(se)}")
#         return jsonify({"error": f"Database error: {str(se)}", "message": None}), 500
#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

# # Get All Users (Only for Admin & Super Admin)
# @auth_bp.route("/all", methods=["GET"])
# @jwt_required()
# def get_all_auth():  # Consider renaming to get_all_users for clarity
#     try:
#         current_user = get_jwt_identity()

#         if current_user["user_type"] not in ["admin", "super_admin"]:
#             return jsonify({"error": "Unauthorized access", "message": None}), 403

#         users = User.query.all()  # Changed 'auth' to 'users' for consistency
#         return jsonify({
#             "message": "Users retrieved successfully",
#             "users": [user.to_dict() for user in users],
#             "error": None
#         }), 200

#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

# # Get User Profile
# @auth_bp.route("/profile", methods=["GET"])
# @jwt_required()
# def get_user_profile():
#     try:
#         current_user = get_jwt_identity()
#         user = User.query.get(current_user["user_id"])

#         if not user:
#             return jsonify({"error": "User not found", "message": None}), 404

#         return jsonify({
#             "message": "Profile retrieved successfully",
#             "user": user.to_dict(),
#             "error": None
#         }), 200

#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

# # Update User Profile
# @auth_bp.route("/update", methods=["PUT"])
# @jwt_required()
# def update_user():
#     try:
#         current_user = get_jwt_identity()
#         user = User.query.get(current_user["user_id"])

#         if not user:
#             return jsonify({"error": "User not found", "message": None}), 404

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No data provided", "message": None}), 400

#         user.name = data.get("name", user.name)      # Use lowercase 'name'
#         user.phone = data.get("phone", user.phone)   # Use lowercase 'phone'
#         user.address = data.get("address", user.address)  # Use lowercase 'address'

#         db.session.commit()

#         return jsonify({
#             "message": "User updated successfully",
#             "user": user.to_dict(),
#             "error": None
#         }), 200

#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

# # Delete User (Only for Admin & Super Admin)
# @auth_bp.route("/delete/<int:user_id>", methods=["DELETE"])
# @jwt_required()
# def delete_user(user_id):
#     try:
#         current_user = get_jwt_identity()

#         if current_user["user_type"] not in ["admin", "super_admin"]:
#             return jsonify({"error": "Unauthorized access", "message": None}), 403

#         user_to_delete = User.query.get(user_id)

#         if not user_to_delete:
#             return jsonify({"error": "User not found", "message": None}), 404

#         if user_to_delete.user_id == current_user["user_id"]:  # Use lowercase 'user_id'
#             return jsonify({"error": "You cannot delete your own account", "message": None}), 403

#         db.session.delete(user_to_delete)
#         db.session.commit()

#         return jsonify({"message": "User deleted successfully", "error": None}), 200

#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500
    

# # Create Admin/Super Admin (Only for existing Admin or Super Admin)
# @auth_bp.route("/create-admin", methods=["POST"])
# @jwt_required()
# def create_admin_user():
#     try:
#         current_user = get_jwt_identity()
#         if current_user["user_type"] not in ["admin", "super_admin"]:
#             return jsonify({"error": "Unauthorized to create admin/super_admin"}), 403

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No data provided"}), 400

#         required_fields = ["name", "email", "phone", "password", "user_type"]
#         if not all(field in data and data[field] for field in required_fields):
#             return jsonify({"error": "Missing required fields"}), 400

#         if data["user_type"] not in ["admin", "super_admin"]:
#             return jsonify({"error": "Only 'admin' or 'super_admin' allowed for this endpoint"}), 400

#         if User.query.filter_by(email=data["email"].lower()).first():
#             return jsonify({"error": "Email already exists"}), 400

#         hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
#         new_user = User(
#             name=data["name"],
#             email=data["email"].lower(),
#             phone=data["phone"],
#             password_hash=hashed_password,
#             user_type=data["user_type"]
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({"message": f"{data['user_type']} created successfully", "user": new_user.to_dict()}), 201

#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": f"Database error: {str(e)}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}"}), 500




from flask import Blueprint, request, jsonify, send_from_directory
from laphic_app.extensions import db, bcrypt, jwt
from laphic_app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import re
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")
CORS(auth_bp, resources={r"/auth/*": {"origins": ["http://localhost:*"]}})  # Allow all localhost ports

# Configure upload folder
UPLOAD_FOLDER = 'uploads/profile_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        print(f"Received request from {request.origin}: {data}") # Enhanced debug log
        if not data:
            return jsonify({"error": "No data provided", "message": None}), 400

        required_fields = ["name", "email", "phone", "password"]
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"error": "All required fields (name, email, phone, password) must be filled", "message": None}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
            return jsonify({"error': 'Invalid email format', 'message": None}), 400
        if not re.match(r"^\+?1?\d{9,15}$", data["phone"]):
            return jsonify({"error": "Invalid phone number format", "message": None}), 400
        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters", "message": None}), 400

        if User.query.filter_by(email=data["email"].lower()).first():
            return jsonify({"error": "Email is already registered", "message": None}), 400

        user_type = data.get("user_type", "user")
        allowed_types = ["user", "customer", "admin", "super_admin"]
        if user_type not in allowed_types:
            return jsonify({"error": "Invalid user type", "message": None}), 400
        if user_type in ["admin", "super_admin"]:
            return jsonify({"error": "Cannot register as admin or super_admin through public endpoint", "message": None}), 403

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        new_user = User(
            name=data["name"],
            email=data["email"].lower(),
            phone=data["phone"],
            password_hash=hashed_password,
            user_type=user_type,
            profile_image=data.get("profile_image")  # Optional, defaults to None
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "user": new_user.to_dict(), "error": None}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        if not data:
            print("No data provided")
            return jsonify({"error": "No data provided", "message": None}), 400

        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()
        print(f"Email: {email}, Password: {'*' * len(password)}")

        if not email or not password:
            print("Email or password missing")
            return jsonify({"error": "Email and password are required", "message": None}), 400

        user = User.query.filter_by(email=email).first()
        print(f"User found: {user}")
        if not user:
            print("User not found")
            return jsonify({"error": "Invalid email or password", "message": None}), 401

        if not bcrypt.check_password_hash(user.password_hash, password):
            print("Password mismatch")
            return jsonify({"error": "Invalid email or password", "message": None}), 401

        access_token = create_access_token(identity={"user_id": user.user_id, "user_type": user.user_type})
        print(f"Token generated: {access_token}")
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": user.to_dict(),
            "error": None
        }), 200

    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
        return jsonify({"error": f"Invalid input: {str(ve)}", "message": None}), 400
    except SQLAlchemyError as se:
        print(f"SQLAlchemyError: {str(se)}")
        return jsonify({"error": f"Database error: {str(se)}", "message": None}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_users():
    try:
        current_user = get_jwt_identity()

        if current_user["user_type"] not in ["admin", "super_admin"]:
            return jsonify({"error": "Unauthorized access", "message": None}), 403

        users = User.query.all()
        return jsonify({
            "message": "Users retrieved successfully",
            "users": [user.to_dict() for user in users],
            "error": None
        }), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["user_id"])

        if not user:
            return jsonify({"error": "User not found", "message": None}), 404

        return jsonify({
            "message": "Profile retrieved successfully",
            "user": user.to_dict(),
            "error": None
        }), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_user():
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["user_id"])

        if not user:
            return jsonify({"error": "User not found", "message": None}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided", "message": None}), 400

        user.name = data.get("name", user.name)
        user.phone = data.get("phone", user.phone)
        user.email = data.get("email", user.email).lower()  # Ensure email is lowercase

        # Validate email if updated
        if "email" in data and not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
            return jsonify({"error": "Invalid email format", "message": None}), 400

        # Check if email is already taken by another user
        if "email" in data:
            existing_user = User.query.filter_by(email=data["email"].lower()).first()
            if existing_user and existing_user.user_id != user.user_id:
                return jsonify({"error": "Email is already registered", "message": None}), 400

        db.session.commit()

        return jsonify({
            "message": "User updated successfully",
            "user": user.to_dict(),
            "error": None
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/update-password", methods=["PUT"])
@jwt_required()
def update_password():
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["user_id"])
        if not user:
            return jsonify({"error": "User not found", "message": None}), 404

        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({"error": "Password is required", "message": None}), 400

        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters", "message": None}), 400

        user.password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        db.session.commit()

        return jsonify({"message": "Password updated successfully", "error": None}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/upload-profile-image", methods=["POST", "DELETE"])
@jwt_required()
def upload_profile_image():
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["user_id"])
        if not user:
            return jsonify({"error": "User not found", "message": None}), 404

        if request.method == "POST":
            if 'image' not in request.files:
                return jsonify({"error": "No image provided", "message": None}), 400

            file = request.files['image']
            if file.filename == '':
                return jsonify({"error": "No file selected", "message": None}), 400

            if not allowed_file(file.filename):
                return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg", "message": None}), 400

            filename = secure_filename(f"{current_user['user_id']}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Remove old image if it exists
            if user.profile_image and os.path.exists(user.profile_image[1:]):  # Remove leading '/'
                os.remove(user.profile_image[1:])

            user.profile_image = f"/{UPLOAD_FOLDER}/{filename}"
            db.session.commit()

            return jsonify({
                "message": "Profile image uploaded successfully",
                "image_url": user.profile_image,
                "error": None
            }), 200

        elif request.method == "DELETE":
            if user.profile_image and os.path.exists(user.profile_image[1:]):
                os.remove(user.profile_image[1:])
            user.profile_image = None
            db.session.commit()

            return jsonify({
                "message": "Profile image removed successfully",
                "image_url": None,
                "error": None
            }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/uploads/profile_images/<filename>", methods=["GET"])
def serve_profile_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@auth_bp.route("/delete/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        current_user = get_jwt_identity()

        if current_user["user_type"] not in ["admin", "super_admin"]:
            return jsonify({"error": "Unauthorized access", "message": None}), 403

        user_to_delete = User.query.get(user_id)

        if not user_to_delete:
            return jsonify({"error": "User not found", "message": None}), 404

        if user_to_delete.user_id == current_user["user_id"]:
            return jsonify({"error": "You cannot delete your own account", "message": None}), 403

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({"message": "User deleted successfully", "error": None}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500

@auth_bp.route("/create-admin", methods=["POST"])
@jwt_required()
def create_admin_user():
    try:
        current_user = get_jwt_identity()
        if current_user["user_type"] not in ["admin", "super_admin"]:
            return jsonify({"error": "Unauthorized to create admin/super_admin", "message": None}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided", "message": None}), 400

        required_fields = ["name", "email", "phone", "password", "user_type"]
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"error": "Missing required fields", "message": None}), 400

        if data["user_type"] not in ["admin", "super_admin"]:
            return jsonify({"error": "Only 'admin' or 'super_admin' allowed for this endpoint", "message": None}), 400

        if User.query.filter_by(email=data["email"].lower()).first():
            return jsonify({"error": "Email already exists", "message": None}), 400

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = User(
            name=data["name"],
            email=data["email"].lower(),
            phone=data["phone"],
            password_hash=hashed_password,
            user_type=data["user_type"],
            profile_image=data.get("profile_image")  # Optional
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"{data['user_type']} created successfully", "user": new_user.to_dict(), "error": None}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}", "message": None}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "message": None}), 500