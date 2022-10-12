import requests
import json
from random import choice
from config import BASE_URL, SLACK_WEBHOOK_URL

route = choice(["dates", "trivia", "math", "years"])
fact_resp = requests.get(f"{BASE_URL}{route}/random").json()
statement = fact_resp["fact"]["statement"]

payload = {
    "text": f"{statement}",
}

# Sends message to Slack channel via webhook URL
requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
