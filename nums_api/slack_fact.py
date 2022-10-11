import requests
import json
from random import choice

BASE_URL = "http://localhost:5001/api/"

# Sends message to specific Slack workspace/channel
webhook_url = "https://hooks.slack.com/services/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"

route = choice(["dates", "trivia", "math", "years"])
fact_resp = requests.get(f"{BASE_URL}{route}/random").json()
statement = fact_resp["fact"]["statement"]

payload = {
    "text": f"{statement}",
}

# Sends message to Slack channel via webhook URL
requests.post(webhook_url, data=json.dumps(payload))
