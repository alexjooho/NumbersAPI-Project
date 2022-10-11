import requests
import json
# put here your webhook_url obtained from the steps above
webhook_url = "https://hooks.slack.com/services/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"

payload = {
    "channel": "#random",
    "username": "I AM A BOT",
    "text": "This is test message.",
    "icon_emoji": ":monkey:"
}
requests.post(webhook_url, data=json.dumps(payload))