from flask import Flask, request
from flask_cors import CORS

from nums_api.config import DATABASE_URL
from nums_api.database import connect_db
from nums_api.trivia.routes import trivia
from nums_api.maths.routes import math
from nums_api.dates.routes import dates
from nums_api.years.routes import years
from nums_api.root.routes import root
from nums_api.tracking.models import Tracking
from nums_api.dates.models import Date
from flask_ngrok2 import run_with_ngrok

from twilio.twiml.messaging_response import MessagingResponse
import requests

# Replace URL with production/live URL
RANDOM_TRIVIA_FACT_URL = "http://localhost:5002/api/trivia/random"

# create app and add configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
run_with_ngrok(app)

if __name__ == "__main__":
    app.run()

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

    # When database is updated, use below line to get fact. When website is live,
    # replace RANDOM_TRIVIA_FACT_URL with production/live URL for random trivia fact
    # response = requests.get(RANDOM_TRIVIA_FACT_URL)
    # When database is updated, delete line directly below
    response = requests.get("http://localhost:5001/api/trivia/1")

    random_fact = response.json()

    # Start our TwiML response
    resp = MessagingResponse()

    # # When database is updated, use this instead to get fact statement
    # # Determine the right reply for this message
    # if txt == 'fact':
    #     resp.message(f"{random_fact['fact']['statement']}")
    # else:
    #     resp.message("Please text 'fact' to get a random fact")

    # When database is updated, delete below if/else statement
    if txt == 'fact':
        resp.message(f"interesting fact for {random_fact['error']['message']}")
    else:
        resp.message("Please type Fact to get a random fact")

    return str(resp)

# allow CORS and connect app to database
CORS(app)
connect_db(app)

