SMS with Twilio
======================
In order to activate SMS functionality, you must set up Ngrok and Twilio.

Set up Ngrok
-------------------
1. $ brew install --cask ngrok
2. Set up an account at ngrok.com
3. Configure auth token with Ngrok
    - https://dashboard.ngrok.com/get-started/setup
4. In venv > lib > flask_ngrok2.py
    - Change port to 5001
        - Search for `5000` and change to `5001`
5. In __init__.py
    - Follow https://github.com/MohamedAliRashad/flask-ngrok2 instructions
    - python3 __init__.py to start ngrok server

Start the localhost and ngrok server
-------------------
1. Start localhost server on port 5001
    - $ flask run -p 5001
2. Start ngrok server
    - $ python3 __init__.py

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
