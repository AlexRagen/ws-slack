import logging
import os

from ws_sdk.web import WS


class WsResources:
    def __init__(self):
        self.ws_cust_connector = WS(url=os.environ.get('WS_URL'),
                                    user_key=os.environ.get('WS_USER_KEY'),
                                    token=os.environ.get('WS_ORG_TOKEN'))

    def is_email_exists_in_ws(self, slack_email: str) -> bool:
        ws_user = None
        try:
            ws_users = self.ws_cust_connector.get_users()['users']
            ws_user = [user for user in ws_users if user['email'] == slack_email][0]
            logging.debug(f"Found name: {ws_user['name']} of email: {slack_email} in WS")
        except KeyError:
            logging.exception("Error getting emails")

        return True if ws_user else False
