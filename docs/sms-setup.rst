SMS with Twilio
======================
In order to activate SMS functionality locally, you must set up Ngrok and Twilio.

Set up Ngrok
-------------------
1. $ brew install --cask ngrok
2. Set up an account at ngrok.com
3. Configure auth token with Ngrok
    - https://dashboard.ngrok.com/get-started/setup

Start the localhost and ngrok server
-------------------
1. Start localhost server on port 5001
    - $ flask run -p 5001
2. Start ngrok server in another terminal
    - $ ngrok http 5001

Setup text messaging with Twilio
-------------------
1. Register an account with Twilio
2. Set up trial phone number
3. Manage your active number
    - Configure messaging service
    - Set webhook to link given by Ngrok followed by `/api/sms`
    - Save settings

--------------------------------------
You should be able to send a text to your Twilio account phone number and
recieve a fact.
