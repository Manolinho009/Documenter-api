from flask import Flask
from flask_cors import CORS



application = Flask(__name__)
application.config['SECRET_KEY'] = 'Jesus'


cors = CORS(app=application, resources={r"/*": {"origins": "*"}})


from app import Routes
