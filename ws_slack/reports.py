import json
import logging
from abc import ABC
from ws_slack import slack_actions
from ws_sdk.web import WS
from ws_sdk.ws_constants import *


class Report(ABC):
    def __init__(self,
                 ws_conn_details: dict,
                 config: dict,
                 ws_connector: WS):
        self.ws_conn_details = ws_conn_details
        self.config = config
        self.ws_connector = ws_connector
        self.report_name = f"{self.__class__.__name__} Report"
        # Report execution
        self.scope, self.channel, self.header_text = self.create_report_metadata()
        if is_valid_config(self.ws_conn_details, self.config['MandatoryWsConnProp'] + self.MANDATORY_PROPS):
            block = self.create_slack_block()
        else:
            KeyError
        slack_actions.send_to_slack(channel=self.channel, block=json.dumps(block))
        logging.info(f"Successfully executed: {self.report_name}")

    def create_report_metadata(self) -> tuple:
        scope = self.ws_connector.get_scope_by_token(token=self.ws_conn_details['ws_scope_token'])
        channel = self.get_channel_name(scope_type=scope['type'], scope_token=self.ws_conn_details['ws_scope_token'])
        header_text = f"{scope['type']} {scope['name']} {self.report_name}"

        return scope, channel, header_text

    def get_channel_name(self, scope_type, scope_token) -> str:
        channel_name = f"{self.config['ChannelPrefix']}{scope_type}_{self.ws_connector.get_scope_name_by_token(token=scope_token)}"

        return slack_actions.fix_slack_channel_name(channel_name)


class Alerts(Report):
    MANDATORY_PROPS = ['ws_scope_token']

    def create_slack_block(self):
        def create_alert_row(a) -> dict:
            l = a['library']
            l['lib_url'] = f"{self.ws_connector.url}/Wss/WSS.html#!libraryDetails;uuid={l['keyUuid']};orgToken={self.ws_connector.token}"

            if a['type'] == AlertTypes.REJECTED_BY_POLICY_RESOURCE:
                text = f"Library rejected due to violation of policy: {a['description']}"
            elif a['type'] == AlertTypes.SECURITY_VULNERABILITY:
                text = f"{a['vulnerability']['severity'].capitalize()} vulnerability {a['vulnerability']['name']} on library"
            else:
                text = f"{a['type']}"

            elements = [{"type": "mrkdwn",
                         "text": f"<{l['lib_url']}|{l['filename']}> - {text}"}]

            return {"type": "context",
                    "elements": elements}

        report_data = self.ws_connector.get_alerts(token=self.ws_conn_details['ws_scope_token'])
        block = [create_header_block(self.header_text),
                 create_mrkdn_block(f"Found {len(report_data)} alerts with vulnerabilities")]

        for i, alert in enumerate(report_data):
            if i + 3 < 50:
                block.append(create_alert_row(alert))
            else:
                logging.warning("More then 50 alerts. Not all alerts will be displayed")
                element = [{"type": "mrkdwn",
                            "text": "..."}]
                block.append({"type": "context",
                              "elements": element})
                break

        return block


class LibVulnerabilities(Report):
    report_name = "Library Vulnerabilities"
    MANDATORY_PROPS = ['ws_scope_token']

    def create_slack_block(self):
        def create_lib_vul_section(l) -> dict:  # TODO: CONTINUE WORKING ON MESSAGE
            l['lib_url'] = f"{self.ws_connector.url}/Wss/WSS.html#!libraryDetails;uuid={l['keyUuid']};orgToken={self.ws_connector.token}"

            elements = [{"type": "mrkdwn",
                         "text": f"<{l['lib_url']}|{l['filename']}> "
                                 f"{print_set(l['vulnerabilities'], 3)}"}]

            return {"type": "context",
                    "elements": elements}

        report_data = self.ws_connector.get_vulnerabilities_per_lib(token=self.ws_conn_details['ws_scope_token'])

        block = [create_header_block(self.header_text),
                 create_mrkdn_block(f"Found {len(report_data)} libraries with vulnerabilities")]
        for lib in report_data:
            block.append(create_lib_vul_section(lib))
            # block.append({"type": "divider"})

        return block


def is_valid_config(matched_dict, mandatory_keys):    # TODO: Add syntax validation and perhaps connectivity test?
    for key in mandatory_keys:
        if matched_dict.get(key) is None:
            logging.error(f"Missing {key}")
            return False
    return True


def create_header_block(header) -> dict:
    return {"type": "header",
            "text": {"type": "plain_text",
                     "text": header,
                     "emoji": True}
            }


def get_sev_icon(severity) -> str:
    return {
        "high": "https://i.imgur.com/7h75Aox.png",
        "medium": "https://i.imgur.com/MtPw8GH.png",
        "low": "https://i.imgur.com/4ZJPTpS.png"
    }[severity]


def create_mrkdn_block(string) -> dict:
    return {"type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{string}"
            }
            }


def create_vul_section(vul, org_details, conn_dict) -> dict:
    lib = vul['library']
    elements = [{"type": "image",
                 "image_url": get_sev_icon(vul['severity']),
                 "alt_text": "Severity"},
                {
                    "type": "mrkdwn",
                    "text": f"<{conn_dict['wss_url']}/Wss/WSS.html#!securityVulnerability;id={vul['name']};orgToken={org_details['orgToken']}|{vul['name']}> - "
                            f"<{conn_dict['wss_url']}/Wss/WSS.html#!libraryDetails;uuid={lib['keyUuid']};orgToken={org_details['orgToken']}|{lib['filename']}>\n"
                            f"*Product:* {vul['product']} *Project:* {vul['project']} *Score:* {vul['score']}"}]

    return {"type": "context",
            "elements": elements}


def print_set(set_to_p, max_e_per_set) -> str:
    ret = []
    if len(set_to_p) < max_e_per_set:
        ret = ', '.join(set_to_p)
    else:
        for i, val in enumerate(set_to_p):
            if i < max_e_per_set:
                ret.append(val)
            else:
                break
        ret = ', '.join(ret) + " ..."

    return ret
