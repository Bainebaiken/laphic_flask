from invix_app import create_app
from flask import Flask
from flask_cors import CORS

# app = Flask(__name__)

app = create_app()
UPLOAD_FOLDER = 'uploads'
# Formamily
# app.config['UPLOAD_FOLDER'] = 'uploads'

# CORS(app) 

# if __name__ == "__main__":
#     app.run(debug=True)




CORS(app)  # This enables CORS for all routes and all origins

@app.route('/api/v1/articles/')
def articles():
    return {'articles': []}  # Example response

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    # Ensure the app runs on 0.0.0.0 if deploying on Render, not localhost
    app.run(debug=True, host='0.0.0.0', port=5000)





