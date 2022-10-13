from flask import Flask, request
from flask_cors import CORS

from nums_api.config import DATABASE_URL, RANDOM_TRIVIA_FACT_URL
from nums_api.database import connect_db
from nums_api.trivia.routes import trivia
from nums_api.maths.routes import math
from nums_api.dates.routes import dates
from nums_api.years.routes import years
from nums_api.root.routes import root
from nums_api.tracking.models import Tracking
from nums_api.dates.models import Date

from twilio.twiml.messaging_response import MessagingResponse
import requests

# create app and add configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# register blueprints
app.register_blueprint(root)
app.register_blueprint(trivia, url_prefix='/api/trivia')
app.register_blueprint(math, url_prefix='/api/math')
app.register_blueprint(dates, url_prefix='/api/dates')
app.register_blueprint(years, url_prefix='/api/years')

# request tracking
@app.after_request
def track_request(response):
    """Track request item and category, update total number of requests in DB."""

    #TODO: Either add logic to handle batch requests or explicitly exclude (once batch requests PRs are complete).

    PATH_SPLIT_INDEX = 5

    #if route was invalid, return response and do not write to DB:
    response_value = response.get_data()
    if not response.json:
        return response

    #ensure route is parsable, otherwise return:
    try:
        [category, req_item] = request.path.lower()[PATH_SPLIT_INDEX:].split("/",1)
    except ValueError:
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

@app.route("/api/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply back to a user from an incoming text message
    If incoming text message is 'fact', user will recieve a random trivia fact text
    If incoming text message is not 'fact', user will recieve a text message
    prompting "Please text 'fact' to get a random fact"
    """
    # Get the message the user sent our Twilio number
    txt = request.values.get('Body').lower()

    response = requests.get(RANDOM_TRIVIA_FACT_URL)

    random_fact = response.json()

    # Start our TwiML response
    resp = MessagingResponse()

    if txt == 'fact':
        resp.message(f"{random_fact['fact']['statement']}")
    else:
        resp.message("Please text 'fact' to get a random fact")

    return str(resp)

# allow CORS and connect app to database
CORS(app)
connect_db(app)

