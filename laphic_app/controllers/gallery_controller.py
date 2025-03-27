from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from laphic_app.models.gallery import Gallery
from laphic_app.extensions import db
import os

# Create a Blueprint for the gallery
gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

# Set a directory for storing uploaded images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a new gallery image
@gallery_bp.route('/add', methods=['POST'])
def add_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Get additional data
        image_name = request.form.get('name')
        image_description = request.form.get('description')
        service_id = request.form.get('service_id')

        # Save to database
        new_image = Gallery(
            Image_Name=image_name,
            Image_Path=file_path,
            Service_ID=service_id,
            Image_Description=image_description
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Image added successfully", "image_id": new_image.Image_ID}), 201
    else:
        return jsonify({"error": "File type not allowed"}), 400

# Get all gallery images
@gallery_bp.route('/all', methods=['GET'])
def get_all_images():
    images = Gallery.query.all()
    image_list = [
        {
            "id": image.Image_ID,
            "name": image.Image_Name,
            "description": image.Image_Description,
            "path": image.Image_Path,
            "upload_date": image.Upload_Date,
            "service_id": image.Service_ID
        }
        for image in images
    ]
    return jsonify(image_list), 200

# Get a specific gallery image by ID
@gallery_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Gallery.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    image_data = {
        "id": image.Image_ID,
        "name": image.Image_Name,
        "description": image.Image_Description,
        "path": image.Image_Path,
        "upload_date": image.Upload_Date,
        "service_id": image.Service_ID
    }
    return jsonify(image_data), 200

# Update a gallery image
@gallery_bp.route('/update/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = Gallery.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    image.Image_Name = request.json.get('name', image.Image_Name)
    image.Image_Description = request.json.get('description', image.Image_Description)
    image.Service_ID = request.json.get('service_id', image.Service_ID)

    db.session.commit()
    return jsonify({"message": "Image updated successfully"}), 200

# Delete a gallery image
@gallery_bp.route('/delete/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Gallery.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    # Delete the file from the file system
    try:
        os.remove(image.Image_Path)
    except FileNotFoundError:
        pass

    # Remove from database
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted successfully"}), 200
