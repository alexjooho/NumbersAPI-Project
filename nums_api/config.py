from cgi import test
import os
from dotenv import load_dotenv

# load .env environment variables
load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL_TEST = os.environ['DATABASE_URL_TEST']

BASE_URL = os.environ['BASE_URL']
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

MAX_BATCH = 50
