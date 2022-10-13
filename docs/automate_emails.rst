How to set up a cron job to automate weekly emails
==================================================

- Automate_email.py will make a get request to the api route to send a email with
the latest weekly updated facts to subscribers.

1. Create a new cron job:
In terminal, type:

    crontab -e

2. Inside the crontab nano editor, set the cron time intervals:
***** (min, hour, day of the month, month, day of the week)
- for reference on how to write cron time intervals, visit https://crontab.guru/

3. Get the path of python:
- type "which python3" in terminal to get absolute path
- alternatively, can use the path of python inside project/venv/bin

4. Get the path of the python sript "automate_email.py"
- your cronjob should look something like this:

    * * * * 7  /path/numbers_api_v2/venv/bin/python  /path/numbers_api_v2/nums_api/automate/automate_email.py

- Save the cronjob and exit

Permissions
-----------

- On some platforms, you may need to grant permissions to cron to run files.

1. Allow filename to run, paste this command in terminal in path/project/ directory that contains script file
(make sure to be in venv)

    chmod 777 automate_email.py

2. Grant full disk access to the terminal

    System Preferences > Security & Privacy > Privacy > Files and Folders
    Click (+) and select Terminal

3. Grant full disk access to cron

    System Preferences > Security & Privacy > Privacy > Files and Folders
    Click (+)
    Press command+shift+G to open the Go to Folder… dialog, type /usr/sbin/cron and press Enter:

Useful commands
---------------

- List existing cron jobs:

    crontab -l

- Delete cron job:

    crontab -r

Debugging
---------

- If your cron job is running into errors, you will get a "mail", to access and read, in terminal type:
(make sure to replace USERNAME with your username)

    cat /var/mail/USERNAME

- To delete your cron mail, you can type:

    > /var/mail/USERNAME
