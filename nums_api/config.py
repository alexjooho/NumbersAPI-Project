import os
from dotenv import load_dotenv

# load .env environment variables
load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL_TEST = os.environ['DATABASE_URL_TEST']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
SECRET_KEY = os.environ['SECRET_KEY']

MAX_BATCH = 50