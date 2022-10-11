import os
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Blueprint
from twilio.twiml.messaging_response

# load .env environment variables
load_dotenv()

sms = Blueprint("sms", __name__)

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
FROM_NUMBER = os.environ['FROM_NUMBER']
TO_NUMBER = os.environ['TO_NUMBER']


client = Client(ACCOUNT_SID, AUTH_TOKEN)

# app = Flask(__name__)

@sms.route("/", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.data.decode('utf8')

    body = body.lower()
    # Start our TwiML response
    # resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'fact':
        msg = "Hi! This works"
    else:
        msg = "Please type Fact to get a random fact"

    message = client.messages.create(
    to=TO_NUMBER,
    from_=FROM_NUMBER,
    body=msg)

    breakpoint()

    return jsonify("hi")