#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint  # , url_for
# from flask_mail import Message

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
html_views = Blueprint('html_views', __name__, url_prefix='/')




# from api.v1.views.index import *
#from utils import send_password_reset_email
from api.v1.views.htmls import *
from api.v1.views.users import *
from api.v1.views.categories import *
from api.v1.views.menu_items import *
from api.v1.views.orders import *
from api.v1.views.order_items import *
from api.v1.views.locations import *
from api.v1.views.payments import *

# Ensure the route is included


# from api.v1.views.send_email import send_email
#from api.v1.app import mail
#from flask_mail import Message
#from flask import url_for

