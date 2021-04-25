import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))


def get_slack_user_email(user_id: str):
    try:
        return get_slack_user_data(user_id).__dict__['data']['user']['profile']['email']
    except KeyError or None:
        logging.exception("Unable to get email address")


def get_slack_user_data(user_id: str):
    try:
        return client.users_info(user=user_id)
    except SlackApiError:
        logging.exception("Error getting user")


def get_all_slack_channels() -> list:
    try:
        return client.conversations_list().__dict__['data']['channels']
    except SlackApiError:
        logging.exception(f"Error fetching channels")


def get_slack_channel(channel_name) -> dict:
    channels = get_all_slack_channels()
    for cur_channel in channels:
        if channel_name == cur_channel['name']:
            logging.debug(f"Channel {channel_name} found")
            return cur_channel

    logging.debug(f"Channel {channel_name} was not found")


def is_slack_channel_exists(channel_name) -> bool:
    return True if get_slack_channel(channel_name) else False


def is_in_slack_channel(channel_name) -> bool:
    channel = get_slack_channel(channel_name)
    return channel['is_member']


def join_channel(channel_name):
    channel_id = get_slack_channel(channel_name)['id']
    client.conversations_join(channel=channel_id)


def create_channel(channel_name, create_private=False):  # TODO CHANGE TO PRIVATE CHANNELS. CURRENTLY GET LIST THEM: https://stackoverflow.com/questions/53736333/slack-conversations-list-method-does-not-list-all-the-channels
    try:
        c = client.conversations_create(name=channel_name, is_private=create_private)
        c_data_dict = c.__dict__['data']['channel']
        r = client.conversations_join(channel=c_data_dict['id'])
        logging.debug(f"Channel {c_data_dict['name']} (ID: {c_data_dict['id']}) created ")
    except SlackApiError:
        logging.exception("Failed to create channel")


def send_to_slack(channel, block):
    if not is_slack_channel_exists(channel):
        create_channel(channel)
    if not is_in_slack_channel(channel):
        join_channel(channel)
    try:
        client.chat_postMessage(channel=channel, blocks=block, text=block)
    except SlackApiError:
        logging.exception("Unable to post to Slack")


# In slack Channel names can’t contain spaces, periods, or most punctuation
def fix_slack_channel_name(channel_name):
    return channel_name.lower() \
        .replace(" ", "_") \
        .replace(".", "_")