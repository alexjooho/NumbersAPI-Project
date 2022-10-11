import requests
import json
from random import choice

# put here your webhook_url obtained from the steps above
webhook_url = "https://hooks.slack.com/services/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"

route = choice(["dates", "trivia", "math", "years"])

fact_resp = requests.get(f"http://localhost:5001/api/{route}/random").json()

statement = fact_resp["fact"]["statement"]

payload = {
    "text": f"{statement}",
}
requests.post(webhook_url, data=json.dumps(payload))
