import requests
import json
from integrate_with_jira import credentials
import logging

log = logging.getLogger(__name__)

XRAY_API = 'https://xray.cloud.getxray.app/api/v2'

XRAY_API_IMPORT_RESULT = 'https://xray.cloud.getxray.app/api/v1'


class XrayAPI:
    def __init__(self):
        self.token = ''

    # generate token with client_id and client_Secret
    def authenticate(self):
        log.debug('Authenticating with Xray API...')

        json_data = json.dumps({"client_id": credentials.CLIENT_ID, "client_secret": credentials.CLIENT_SECRET})

        resp = requests.post(f'{XRAY_API}/authenticate', data=json_data, headers={'Content-Type': 'application/json'})
        resp.raise_for_status()

        self.token = 'Bearer ' + resp.text.replace("\"", "")

    # generate new test execution
    def generateTestExecution(self, results, projectId, issueTypeName, fixVersionNames, summary):
        log.debug(f'Creating Test Execution "{summary}"...')
        fixVersions = list(map(lambda versioName: {"name": versioName}, fixVersionNames))
        data = {

            "fields": {
                "project": {
                    "id": projectId
                },
                "issuetype": {
                    "name": issueTypeName
                },
                "summary": summary,
                "fixVersions": fixVersions
            }
        }
        json_data = json.dumps(data)

        resp = requests.post(f'{XRAY_API}/import/execution/robot/multipart',
                             files={'results': results, 'info': json_data},
                             headers={'Authorization': self.token})
        resp.raise_for_status()

        return resp.json()

    # import result to test execution
    def importRobotResults(self, results):
        log.debug(f'Import Test Execution ...')

        resp = requests.post(
            f'{XRAY_API_IMPORT_RESULT}/import/execution/robot?testExecKey={credentials.TEST_EXECUTION_KEY}',
            data=results, headers={'Content-Type': 'application/xml', 'Authorization': self.token})
        resp.raise_for_status()

        return resp.json()
