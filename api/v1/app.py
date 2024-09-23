#!/usr/bin/python3
""" Flask Application """
from os import environ
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from api.v1.mail_setup import mail
from models import storage
#from api.v1.views import app_views, html_views
import os



load_dotenv()


# from flasgger.utils import swag_from


# app = Flask(__name__, static_folder='../../web_dynamic/static', template_folder='../../web_dynamic/templates')
app = Flask(__name__, static_folder='../../static', template_folder='../../templates')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_TLS'] = True

mail.init_app(app)  # Initialize mail with app

"""
with app.app_context():
    msg = Message('Test Email',
                  sender='takeabite56@gmail.com',
                  recipients=['adwoaserwahkyeibaffour@gmail.com',
                              'lindseylinwood56@gmail.com'])
    msg.body = 'This is a test email.'
    try:
        mail.send(msg)
        print("Test email sent.")
    except Exception as e:
        print(f"Error sending test email: {e}")
"""

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

from api.v1.views import app_views, html_views
app.register_blueprint(app_views)
app.register_blueprint(html_views) 
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configure session secret key from environment
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configure paystack secret key from environment
paystack_secret_key = os.getenv('PAYSTACK_SECRET_KEY')


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'Take-A-Bite Restful API',
    'uiversion': 1
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5005'
    app.run(host=host, port=port, threaded=True, debug=True)
