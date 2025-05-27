from flask import Blueprint, request, jsonify, send_from_directory
from laphic_app.extensions import db
from laphic_app.models.gallery import Gallery
from werkzeug.utils import secure_filename
import os

gallery_bp = Blueprint('gallery', __name__, url_prefix='/api/gallery')

# Directory for storing images
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Get all gallery images
@gallery_bp.route('/all', methods=['GET'])
def get_all_images():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    images = Gallery.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [img.to_dict() for img in images.items],
        'total': images.total,
        'pages': images.pages,
        'page': page
    }), 200

# Get gallery images by service ID
@gallery_bp.route('/service/<int:service_id>', methods=['GET'])
def get_images_by_service(service_id):
    category = request.args.get('category')
    query = Gallery.query.filter_by(Service_ID=service_id)
    if category:
        query = query.filter_by(Category=category)
    images = query.all()
    return jsonify([img.to_dict() for img in images]), 200

# Get a single image by ID
@gallery_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Gallery.query.get_or_404(image_id)
    return jsonify(image.to_dict()), 200

# Add a new image with file upload
@gallery_bp.route('/upload', methods=['POST'])
def add_image():
    if 'image' not in request.files or not request.form.get('Service_ID') or not request.form.get('Image_Name'):
        return jsonify({"error": "Missing image or required fields"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        new_image = Gallery(
            Service_ID=int(request.form.get('Service_ID')),
            Image_Name=request.form.get('Image_Name'),
            Image_Description=request.form.get('Image_Description', ''),
            Image_Path=filename,  # Store just the filename
            Min_Cost=request.form.get('Min_Cost', type=float),
            Max_Cost=request.form.get('Max_Cost', type=float),
            Min_Square_Meters=request.form.get('Min_Square_Meters', type=float),
            Max_Square_Meters=request.form.get('Max_Square_Meters', type=float),
            Category=request.form.get('Category')
        )
        db.session.add(new_image)
        db.session.commit()
        return jsonify(new_image.to_dict()), 201
    else:
        return jsonify({"error": "Invalid file type"}), 400

# Update an image
@gallery_bp.route('/update/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = Gallery.query.get_or_404(image_id)
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    image.Image_Name = data.get('Image_Name', image.Image_Name)
    image.Image_Description = data.get('Image_Description', image.Image_Description)
    image.Image_Path = data.get('Image_Path', image.Image_Path)
    image.Min_Cost = data.get('Min_Cost', image.Min_Cost)
    image.Max_Cost = data.get('Max_Cost', image.Max_Cost)
    image.Min_Square_Meters = data.get('Min_Square_Meters', image.Min_Square_Meters)
    image.Max_Square_Meters = data.get('Max_Square_Meters', image.Max_Square_Meters)
    image.Category = data.get('Category', image.Category)

    db.session.commit()
    return jsonify(image.to_dict()), 200

# Delete an image
@gallery_bp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Gallery.query.get_or_404(image_id)
    # Optionally delete the image file from the server
    if image.Image_Path and os.path.exists(os.path.join(UPLOAD_FOLDER, image.Image_Path)):
        os.remove(os.path.join(UPLOAD_FOLDER, image.Image_Path))
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted"}), 200

# Serve images
@gallery_bp.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)






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
