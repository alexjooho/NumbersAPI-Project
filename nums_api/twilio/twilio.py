import os
from twilio.rest import Client
from dotenv import load_dotenv
from flask import request, Blueprint, jsonify
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from nums_api.maths.models import Math
from nums_api.trivia.models import Trivia
from nums_api.years.models import Year
from nums_api.dates.models import Date

# from flask_ngrok import run_with_ngrok

# load .env environment variables
load_dotenv()

sms = Blueprint("sms", __name__)

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
FROM_NUMBER = os.environ['FROM_NUMBER']
TO_NUMBER = os.environ['TO_NUMBER']

client = Client(ACCOUNT_SID, AUTH_TOKEN)

RANDOM_TRIVIA_FACT_URL = "http://localhost:5002/api/trivia/random"

# app = Flask(__name__)

@sms.route("/", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    # txt = request.values.get('Text')

    print("THIS IS THE TXT")

    # body = request.data.decode('utf8').lower()

    # response = requests.get("http://localhost:5001/api/math/1")

    # random_fact = response.json()

    # Returns json:
    #         { fact:{
    #             "number" : number,
    #             "fragment" : "fragment",
    #             "statement" : "statement",
    #             "type" : "type"
    #         }}


    # Start our TwiML response
    resp = MessagingResponse()
    resp.message("Hello")
    # Determine the right reply for this message
    # if body == 'fact':
    #     resp.message(f"interesting fact for {random_fact['error']['message']}")

    # else:
    #     resp.message("Please type Fact to get a random fact")


    return str(resp)


# if __name__ == "__main__":
#     sms.run()

    # message = client.messages.create(
    # to=TO_NUMBER,
    # from_=FROM_NUMBER,
    # body=random_fact['error']['message'])

    # return jsonify("hi")
