from flask import Blueprint,request,jsonify
from authors_app.models.user import User  
from authors_app.extensions import db,bcrypt
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, get_jwt_identity

#auth Blueprint
auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth')


@auth.route('/register',methods=['POST'])
#creating a function for use register
def register():
    #storing viables
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    contact=request.json['contact']
    user_type=request.json['user_type']
    image=request.json['image']
    password = request.json['password']
    biography = request.json['biography']

    #checking the null validations and  null contraints
    # first approach for lito viables
    #it only for field/viables dat are required only, neccessary/complusary
    if not first_name:
        return jsonify({'error':"Your first_name is required"})
    if not last_name:
        return jsonify({'error':"Your last_name is required"})
    if not email:
        return jsonify({'error':"Your email is required"})
    if not contact:
        return jsonify({'error':"Your contact is required"})
    if not user_type:
        return jsonify({'error':"Your user_type is required"})
    if not image:
        return jsonify({'error':"Your image is required"})
    if len(password)<8:
        return jsonify({'error':"Your password still short"})
    #only if u are not an author
    if user_type == 'author' and not biography:
        return jsonify({'error':"Your biography is required"})
    #searching whthr the email exists 
    if User.query.filter_by(email=email).first():
        return jsonify({'error':"email already exists"})
    if User.query.filter_by(contact=contact).first():
        return jsonify({'error':"contact already exists"})
    

    try:
      #hashing the password
      hashed_password =bcrypt.generate_password_hash(password)
      #creating auser
      new_user = User(first_name=first_name,last_name=last_name,password =hashed_password,email=email,contact=contact,user_type=user_type,image=image)
      db.session.add(new_user)
      db.session.commit()
      # defining avariable that gives track to the user name
      
      username=User.get_full_name() 
      return jsonify({
          'message':username+'has been successfully created as an'+User.user_type,
          'user':{
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "password": new_user.password,
            "email": new_user.email,
            "contact": new_user.contact,
            "image":image,
            "User-type": new_user.user_type,
            "biography": new_user.biography,
            "created_at": new_user.created_at,
            
          }
      })
    
    except KeyError as e:
        # Handle the case where a required field is missing in the request body
        return jsonify({'error': f'Missing {e.args[0]} in request body'})

    except Exception as e:
     db.session.rollback()
     return jsonify({'error':str(e)}) 
    
@auth.route("/<int:id>") 
@jwt_required()
def get_book(id):
    try:
        current_user = get_jwt_identity()  # Get current user using get_jwt_identity
        book = User.query.filter_by(user_id=current_user, id=id).first()

        if not book:
            return jsonify({'error': 'Item not found'}), 404
        
        # Return book details
        return jsonify({
            'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'contact': current_user.contact,
                ' user_type': current_user.user_type,
                'biography': current_user.biography,
                'image':current_user.image,
                'password':current_user.password,
                'created_at': current_user.created_at,
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
    
#defining a login endpoint
@auth.route('/login', methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        #retrieving the user by email
        User = User.query.filter_by(email=email).first()
        # Check if the user exists and the password is correct
        if User and bcrypt.check_password_hash(User.password, password):
            # Return a success response
            return jsonify({'message': 'Login successful', 'user_id': User.id}), 200
        else:
            # Return an error response if authentication fails
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Define the edit user endpoint
@auth.route('/edit/<int:user_id>', methods=["PUT"])
def edit_user(user_id):
    try:
        # Extract user data from the request JSON
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update user fields if provided in the request
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if the new email already exists
            new_email = data['email']
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'The email already exists'}), 400
            user.email = new_email
        if 'image' in data:
            user.image = data['image']
        if 'biography' in data:
            user.biography = data['biography']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'password' in data:
            password = data['password']
            if len(password) < 8:
                return jsonify({'error': 'Password must have at least 8 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if 'contact' in data:
            user.contact = data['contact']    
       # Commit the session to save the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
       
## Define the delete user endpoint
@auth.route('/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit() #pushes to the database

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
     
@auth.route('/users', methods=["GET"])
def get_all_users():
    try:
        # Query all users from the database
        users = User.query.all()

        # Serialize users data im other words convert data into a format suitable for storage
        serialized_users = []
        for user in users:
            serialized_user = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'image': user.image,
                'biography': user.biography,
                'user_type': user.user_type,
                'contact': user.contact,
                'password':user.password
            }
            serialized_users.append(serialized_user)

        # Return the serialized users data
        return jsonify({'users': serialized_users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@auth.route('/user/<int:user_id>', methods=["GET"])
def get_user(user_id):
    try:
        # Query the user from the database by user ID
        user = User.query.get(user_id)

        # Check if the user exists
        if user:
            # Serialize the user data
            serialized_user = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'image': user.image,
                'biography': user.biography,
                'user_type': user.user_type,
                'contact': user.contact,
                'password': user.password
            }
            # Return the serialized user data
            return jsonify({'user': serialized_user}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500   
            
