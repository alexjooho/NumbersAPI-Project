## Daily Random Number Fact for Slack

### Environment Variables:
- `BASE_URL`: API URL for making GET requests. 
- `SLACK_WEBHOOK_URL`: Webhook URL from the Slack app connected to a specific Slack channel.
    - Example: https://hooks.slack.com/services/T01ERXXXXXX/B020XXXXXX/rzrCkTvsXXXXXXXXXXXXXXXX


### Cronjob Automation Instructions:
1. In the terminal, enter `chmod +x slack_fact.py` to make this file executable by all users.
2. To create a cronjob, enter `crontab -e` to enter the cron table. 
3. In a single line, enter `0 12 * * * [absolute path to python executable] [absolute path to slack_fact.py]`
    - This command executes `slack_fact.py` daily at 12pm.
    - Example: `0 12 * * * /Users/username/Desktop/numbers_api_v2/venv/bin/python /Users/username/Desktop/numbers_api_v2/nums_api/slack_fact.py`
        - Note: This command must be on one line in the cron table. 