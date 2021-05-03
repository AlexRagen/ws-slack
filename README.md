![Logo](https://whitesource-resources.s3.amazonaws.com/ws-sig-images/Whitesource_Logo_178x44.png)  

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/whitesourcetools/ws4s)
[![WS Slack Integration](https://github.com/whitesource-ps/ws-slack/actions/workflows/ci.yml/badge.svg)](https://github.com/whitesource-ps/ws-slack/actions/workflows/ci.yml)
[![Python 3.6](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Blue_Python_3.6%2B_Shield_Badge.svg/86px-Blue_Python_3.6%2B_Shield_Badge.svg.png)](https://www.python.org/downloads/release/python-360/)

# WhiteSource Slack Integration 
Service that mediates between WS and Slack and provides WhiteSource reports into a Slack channel.

## Supported reports:
* Organization, Product, and Project level Libraries Vulnerabilities Report - Getting Vulnerabilities per library to Slack Channel.

### Supported methods to produce reports:
_Note: Reports will be written into a dedicated channel in form of: ws\_\_[SCOPE_NAME_IN_LOWERCASE]_

#### Accepting endpoint requests (e.g. from pipelines):
* URL: `https://<URL>/fetch/<REPORT_NAME>`

* The request body should contain:
    ```
       {
        "ws_user_key" : "<userKey>",
        "ws_org_token": "<orgToken>",
        "ws_url": "saas",
        "key": "<value>"...
       }
    ```
#### Accepting Slack slash commands (/ws4s):
* Supported commands:

    ```
    /ws4s token <SCOPE NAME> - Get token ids
    /ws4s <REPORT NAME> <TOKEN>
    ```

## Prerequisites
1. Create Custom App in [Slack API](https://api.slack.com/apps?new_app=1) with the following permissions:
    * Slash commands:
        * Command: /ws4s
        * Request URL: https://<PUBLIC URL>/slack/commands
        * Short Description: Router for ws4S
        * Usage Hint: Report Scope_Name
        * Escape channels, users, and links sent to your app: Checked
    * Bots:
        * App Display Name:
            * Display Name: WS4S
            * Default username: ws4s
1. In Slack application, add WS4S by choosing WS4S in Apps.
    
## Docker Installation and Run options
* Install the container from DockerHub: `docker pull ws-slack` **[TBD]**
```
docker pull whitesourcetools/ws4s
docker run --name ws4s -p 8000:8000 -e SLACK_BOT_TOKEN=xoxb-<TOKEN> -e SLACK_SIGNING_SECRET=<SECRET> whitesourcetools/ws4s
```
