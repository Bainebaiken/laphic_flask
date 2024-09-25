from invix_app import create_app
from flask import Flask
from flask_cors import CORS


app = create_app()
UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = 'uploads'

# CORS(app) 

# if __name__ == "__main__":
#     app.run(debug=True)



# app = Flask(__name__)
CORS(app)  # This enables CORS for all routes and all origins

@app.route('/api/v1/articles/')
def articles():
    return {'articles': []}  # Example response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)





