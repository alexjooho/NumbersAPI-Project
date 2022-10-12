from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail

from nums_api.config import DATABASE_URL, EMAIL_PASSWORD, SECRET_KEY
from nums_api.database import connect_db
from nums_api.trivia.routes import trivia
from nums_api.maths.routes import math
from nums_api.dates.routes import dates
from nums_api.years.routes import years
from nums_api.root.routes import root
from nums_api.tracking.models import Tracking
from nums_api.dates.models import Date
from nums_api.mail.emails import emails

# create app and add configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY


# flask-mail config
# creating instance here (if not get key error mail) but not imported so ???
# cant access class methods connect and send...
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'r27numbersapi@gmail.com'
app.config['MAIL_PASSWORD'] = 'ajhnmxljpktmupks'
app.config['MAIL_DEFAULT_SENDER'] = 'r27numbersapi@gmail.com'
app.config['MAIL_SUPPRESS_SEND'] = app.testing
app.config['MAIL_DEBUG'] = app.debug
mail = Mail(app)

# register blueprints
app.register_blueprint(root)
app.register_blueprint(trivia, url_prefix='/api/trivia')
app.register_blueprint(math, url_prefix='/api/math')
app.register_blueprint(dates, url_prefix='/api/dates')
app.register_blueprint(years, url_prefix='/api/years')
app.register_blueprint(emails, url_prefix='/api/emails')

# request tracking
@app.after_request
def track_request(response):
    """Track request item and category, update total number of requests in DB."""

    #TODO: Either add logic to handle batch requests or explicitly exclude (once batch requests PRs are complete).

    PATH_SPLIT_INDEX = 5

    #if route was invalid, return response and do not write to DB:
    try:
        response_value = response.get_data()
        if not response.json:
            return response
    except:
        print("css error")

    #ensure route is parsable, otherwise return:
    try:
        [category, req_item] = request.path.lower()[PATH_SPLIT_INDEX:].split("/",1)
    except ValueError:
        print('enter')
        return response

    #ignore responses for random:
    if req_item == "random":
        return response

    #convert dates to whole numbers:
    if category == "dates":
        [month, day] = req_item.split("/")
        req_item = Date.date_to_day_of_year(int(month), int(day))

    #write to DB:
    Tracking.update_request_count(req_item, category)

    return response


# allow CORS and connect app to database
CORS(app)
connect_db(app)

