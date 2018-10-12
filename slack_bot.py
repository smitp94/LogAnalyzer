import os
import time
import re
from slackclient import SlackClient


slack_client = SlackClient('xoxb-455104885364-455108551044-OeQX2Psl2NGBsQOaK8CojYmi')
starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
API = 'https://slack.com/api'


def start():
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        # print(starterbot_id)
        # while True:
        #     command, channel = parse_bot_commands(slack_client.rtm_read())
        #     if command:
        #         handle_command(command, channel)
        #     time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


start()
