from integrate_with_jira import credentials
import requests
import json
import logging

log = logging.getLogger(__name__)

PROJECT_TYPE = 'com.pyxis.greenhopper.jira:gh-simplified-scrum-classic'


# get information of account
def searchUser(query):
    log.debug(f'Searching users with "{query}"...')
    resp = requests.get(f'{credentials.INSTANCE}/rest/api/3/user/search?query={query}',
                        auth=(credentials.USER, credentials.TOKEN), headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information of project
def searchProject(query):
    log.debug(f'Searching project with project key "{query}"...')
    resp = requests.get(f'{credentials.INSTANCE}/rest/api/latest/project/{query}',
                        auth=(credentials.USER, credentials.TOKEN), headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information summary of issue
def getIssueSummary(query):
    log.debug('Getting Issue  ...')
    resp = requests.get(
        f'{credentials.INSTANCE}/rest/api/2/search?jql=project={query}&fields=summary',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information issue type of issue
def getIssueType(query):
    log.debug('Getting Issue  ...')
    resp = requests.get(
        f'{credentials.INSTANCE}/rest/api/2/search?jql=project={query}&fields=issuetype',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information status of issue
def getIssueStatus(query):
    log.debug('Getting Issue Status ...')
    resp = requests.get(
        f'{credentials.INSTANCE}rest/api/2/issue/{query}?fields=status',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information fix version of issue
def getIssueFixVersion(query):
    log.debug('Getting Issue Fix Version ...')
    resp = requests.get(
        f'{credentials.INSTANCE}rest/api/2/issue/{query}?fields=fixVersions',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information priority of issue
def getIssuePriority(query):
    log.debug('Getting Issue Fix Priority ...')
    resp = requests.get(
        f'{credentials.INSTANCE}rest/api/2/issue/{query}?fields=priority',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information of board
def getBoard():
    log.debug('Getting Board ...')
    resp = requests.get(
        f'{credentials.INSTANCE}rest/agile/1.0/board',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information of sprint using board id
def getSprint(BroadId):
    log.debug('Getting Sprint ...')
    resp = requests.get(
        f'{credentials.INSTANCE}rest/agile/1.0/board/{BroadId}/sprint',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# get information bug links of test case
def BugKey(testKey):
    log.debug('Getting key of bug ...')
    resp = requests.get(
        f'{credentials.INSTANCE}rest/api/2/issue/{testKey}?fields=issuelinks',
        auth=(credentials.USER, credentials.TOKEN),
        headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
    return resp.json()


# create bug and link with test case corresponding
def createBug(summary, description, projectId, issueTypeName, fixVersionNames, issueLinkKey, priority):
    log.debug(f'Creating Issue "{summary}"...')
    fixVersions = list(map(lambda versioName: {"name": versioName}, fixVersionNames))
    data = {

        "fields": {
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": description,
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "project": {
                "id": projectId
            },
            "issuetype": {
                "name": issueTypeName
            },
            "priority": {
                "name": priority
            },
            "fixVersions": fixVersions,
            "labels": ["default"]
        },
        "update": {
            "issuelinks": [
                {
                    "add": {
                        "type": {
                            "name": "Blocks",
                            "inward": "is blocked by",
                            "outward": "blocks"
                        },
                        "outwardIssue": {
                            "key": issueLinkKey
                        }
                    }
                }
            ]
        }

    }
    json_data = json.dumps(data)

    resp = requests.post(f'{credentials.INSTANCE}/rest/api/3/issue', auth=(credentials.USER, credentials.TOKEN),
                         data=json_data, headers={'Content-Type': 'application/json'})
    resp.raise_for_status()

    return resp.json()


# add issue to sprint
def addIssueToSprint(sprintId):
    log.debug(f'Add issue "" to sprint "{credentials.SPRINT}" ')
    data = {
        "issues": credentials.ISSUE
    }
    json_data = json.dumps(data)
    resp = requests.post(f'{credentials.INSTANCE}/rest/agile/1.0/sprint/{sprintId}/issue',
                         auth=(credentials.USER, credentials.TOKEN),
                         data=json_data, headers={'Content-Type': 'application/json'})
    resp.raise_for_status()
