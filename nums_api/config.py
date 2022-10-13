import os
from dotenv import load_dotenv

# load .env environment variables
load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL_TEST = os.environ['DATABASE_URL_TEST']

MAX_BATCH = 50

RANDOM_TRIVIA_FACT_URL = "http://localhost:5001/api/trivia/random"