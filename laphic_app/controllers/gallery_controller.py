from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models.gallery import Gallery

gallery_bp = Blueprint('gallery', __name__, url_prefix='/api/gallery')

# Get all gallery images
@gallery_bp.route('/', methods=['GET'])
def get_all_images():
    images = Gallery.query.all()
    return jsonify([img.to_dict() for img in images]), 200

# Get gallery images by service ID
@gallery_bp.route('/service/<int:service_id>', methods=['GET'])
def get_images_by_service(service_id):
    images = Gallery.query.filter_by(Service_ID=service_id).all()
    return jsonify([img.to_dict() for img in images]), 200

# Get a single image by ID
@gallery_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Gallery.query.get_or_404(image_id)
    return jsonify(image.to_dict()), 200

# Add a new image
@gallery_bp.route('/', methods=['POST'])
def add_image():
    data = request.json
    new_image = Gallery(
        Service_ID=data.get('Service_ID'),
        Image_Name=data['Image_Name'],
        Image_Description=data.get('Image_Description'),
        Image_Path=data['Image_Path'],
        Min_Cost=data.get('Min_Cost'),
        Max_Cost=data.get('Max_Cost'),
        Min_Square_Meters=data.get('Min_Square_Meters'),
        Max_Square_Meters=data.get('Max_Square_Meters')
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify(new_image.to_dict()), 201

# Update an image
@gallery_bp.route('/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = Gallery.query.get_or_404(image_id)
    data = request.json

    image.Image_Name = data.get('Image_Name', image.Image_Name)
    image.Image_Description = data.get('Image_Description', image.Image_Description)
    image.Image_Path = data.get('Image_Path', image.Image_Path)
    image.Min_Cost = data.get('Min_Cost', image.Min_Cost)
    image.Max_Cost = data.get('Max_Cost', image.Max_Cost)
    image.Min_Square_Meters = data.get('Min_Square_Meters', image.Min_Square_Meters)
    image.Max_Square_Meters = data.get('Max_Square_Meters', image.Max_Square_Meters)

    db.session.commit()
    return jsonify(image.to_dict()), 200

# Delete an image
@gallery_bp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Gallery.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted"}), 200







# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
# from laphic_app.models.gallery import Gallery
# from laphic_app.extensions import db
# import os

# # Create a Blueprint for the gallery
# gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

# # Set a directory for storing uploaded images
# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # Utility function to check allowed file types
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Create a new gallery image
# @gallery_bp.route('/add', methods=['POST'])
# def add_image():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part in the request"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(file_path)

#         # Get additional data
#         image_name = request.form.get('name')
#         image_description = request.form.get('description')
#         service_id = request.form.get('service_id')

#         # Save to database
#         new_image = Gallery(
#             Image_Name=image_name,
#             Image_Path=file_path,
#             Service_ID=service_id,
#             Image_Description=image_description
#         )
#         db.session.add(new_image)
#         db.session.commit()

#         return jsonify({"message": "Image added successfully", "image_id": new_image.Image_ID}), 201
#     else:
#         return jsonify({"error": "File type not allowed"}), 400

# # Get all gallery images
# @gallery_bp.route('/all', methods=['GET'])
# def get_all_images():
#     images = Gallery.query.all()
#     image_list = [
#         {
#             "id": image.Image_ID,
#             "name": image.Image_Name,
#             "description": image.Image_Description,
#             "path": image.Image_Path,
#             "upload_date": image.Upload_Date,
#             "service_id": image.Service_ID
#         }
#         for image in images
#     ]
#     return jsonify(image_list), 200

# # Get a specific gallery image by ID
# @gallery_bp.route('/<int:image_id>', methods=['GET'])
# def get_image(image_id):
#     image = Gallery.query.get(image_id)
#     if not image:
#         return jsonify({"error": "Image not found"}), 404

#     image_data = {
#         "id": image.Image_ID,
#         "name": image.Image_Name,
#         "description": image.Image_Description,
#         "path": image.Image_Path,
#         "upload_date": image.Upload_Date,
#         "service_id": image.Service_ID
#     }
#     return jsonify(image_data), 200

# # Update a gallery image
# @gallery_bp.route('/update/<int:image_id>', methods=['PUT'])
# def update_image(image_id):
#     image = Gallery.query.get(image_id)
#     if not image:
#         return jsonify({"error": "Image not found"}), 404

#     image.Image_Name = request.json.get('name', image.Image_Name)
#     image.Image_Description = request.json.get('description', image.Image_Description)
#     image.Service_ID = request.json.get('service_id', image.Service_ID)

#     db.session.commit()
#     return jsonify({"message": "Image updated successfully"}), 200

# # Delete a gallery image
# @gallery_bp.route('/delete/<int:image_id>', methods=['DELETE'])
# def delete_image(image_id):
#     image = Gallery.query.get(image_id)
#     if not image:
#         return jsonify({"error": "Image not found"}), 404

#     # Delete the file from the file system
#     try:
#         os.remove(image.Image_Path)
#     except FileNotFoundError:
#         pass

#     # Remove from database
#     db.session.delete(image)
#     db.session.commit()
#     return jsonify({"message": "Image deleted successfully"}), 200
