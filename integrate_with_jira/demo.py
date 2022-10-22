import os

import jira
import xray
from integrate_with_jira import credentials
import sys
import logging
from requests.exceptions import HTTPError
import argparse
import xml.etree.ElementTree as ET

log = logging.getLogger('demo')
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


class Scope:
    def __init__(self):
        self.accountId = ''
        self.projectKey = credentials.KEY
        self.projectId = ''


def setup(scope):
    log.info('[Setup]')
    users = jira.searchUser(credentials.USER)
    user = next(filter(lambda u: u['emailAddress'] == credentials.USER, users), None)
    if user:
        accountId = user['accountId']
        scope.accountId = accountId
    else:
        raise Exception('Could\'t find default user!')
    xrayApi = xray.XrayAPI()
    xrayApi.authenticate()
    return xrayApi


def infoProject(scope):
    log.info('[Get info Project Key and Project ID for Setup]')
    users = jira.searchProject(scope.projectKey)
    projectId = users['id']
    scope.projectId = projectId


# function to generate test execution
def importRobotResults(data, scope, xray):
    log.info('[Creating Test Execution ' + credentials.NAME_TEST_EXECUTION + " ]")
    summary = credentials.NAME_TEST_EXECUTION
    projectId = scope.projectId
    issueTypeName = "Test Execution"
    fixVersions = credentials.FIX_VERSION_TEST_EXECUTION
    xray.generateTestExecution(data, projectId, issueTypeName, fixVersions, summary)


# pars file output.xml get test key of test case fail
def ParsXMLPickTestKeyFail():
    tree = ET.parse(credentials.PATH_OUTPUT_ROBOT_FRAMEWORK)
    root = tree.getroot()
    count = 0
    x = []
    for elm in root.findall("./suite/test/tag"):
        x.append(elm.text)
    k = []
    for elm in root.findall("./suite/test/status"):
        k.append(elm.attrib["status"])
    c = []
    for status in k:
        if status == 'FAIL':
            c.append(x[count])
        count = count + 1
    return c


# pars file output.xml get test key of test case
def ParsXMLPickTestKey():
    tree = ET.parse(credentials.PATH_OUTPUT_ROBOT_FRAMEWORK)
    root = tree.getroot()
    arr = []
    for elm in root.findall("./suite/test/tag"):
        arr.append(elm.text)
    return arr


# get issue key of issue with summary
def getKeyOfIssue(summary):
    global key
    x = jira.getIssueSummary(credentials.KEY)
    lists = x['issues']
    for i in range(len(lists)):
        if lists[i].get("fields").get("summary") == summary:
            key = lists[i]['key']
    return key


# get summary of issue with issue key
def getSummaryOfIssue(issueKey):
    global summary
    x = jira.getIssueSummary(credentials.KEY)
    lists = x['issues']
    for i in range(len(lists)):
        if lists[i].get('key') == issueKey:
            summary = lists[i].get("fields").get("summary")
    return summary


# get list issue key with name issue type
def getTestKey(name):
    x = jira.getIssueType(credentials.KEY)
    arrTestKey = []
    lists = x['issues']
    for i in range(len(lists)):
        if lists[i].get('fields').get('issuetype')['name'] == name:
            arrTestKey.append(lists[i]['key'])
    return arrTestKey


# get board id with project key
def getBoardIdOfProjectKey():
    global boardId
    x = jira.getBoard()
    lists = x['values']
    for i in range(len(lists)):
        if lists[i].get("name") == credentials.KEY + " board":
            boardId = lists[i]['id']
    return boardId


# get sprint id with board id
def getSprintIdOfBoard():
    global sprintId
    x = jira.getSprint(getBoardIdOfProjectKey())
    lists = x['values']
    for i in range(len(lists)):
        if lists[i].get("name") == credentials.SPRINT:
            sprintId = lists[i]['id']
    return sprintId


def getStatusIssue(issueKey):
    x = jira.getIssueStatus(issueKey)
    status = x['fields']['status']['name']
    return status


def getStatusFixVersion(issueKey):
    x = jira.getIssueFixVersion(issueKey)
    fixVersion = x['fields']['fixVersions']
    arr = []
    for i in range(len(fixVersion)):
        arr.append(fixVersion[i].get("name"))
    return arr


def getStatusPriority(issueKey):
    x = jira.getIssuePriority(issueKey)
    priority = x['fields']['priority']['name']
    return priority


def createBug(scope, summaryBug, fixVersion, issueLinkKey, priority):
    log.info('[Creating Bug ' + summaryBug + " ]")

    summary = "Bug " + summaryBug
    description = "Bug " + summaryBug
    projectId = scope.projectId
    issueTypeName = "Bug"
    fixVersions = fixVersion
    jira.createBug(summary, description, projectId, issueTypeName, fixVersions, issueLinkKey, priority)
    return scope


# get key of bug with key of test case fail
def getBugKey(testKey):
    global bugKey
    x = jira.BugKey(testKey)
    lists = x['fields']['issuelinks']
    if len(lists) != 0:
        for i in range(len(lists)):
            if lists[i].get('inwardIssue')['fields']['issuetype']['name'] == 'Bug':
                bugKey = lists[i].get('inwardIssue')['key']
    else:
        bugKey = "empty"
    return bugKey


def checkAndCreateBug(scope):
    if len(ParsXMLPickTestKeyFail()) != 0:
        for i in ParsXMLPickTestKeyFail():
            if getBugKey(i) == "empty":
                createBug(scope, getSummaryOfIssue(i), credentials.FIX_VERSION_BUG, i, credentials.MEDIUM)
            else:
                print("[" + getSummaryOfIssue(getBugKey(i)) + " ---- was Existed\n"
                                                              "Status: " + getStatusIssue(getBugKey(i)) + "\n"
                                                                                                          "Priority: " + getStatusPriority(
                    getBugKey(i)) +
                      "\nFix Versions:")
                print(getStatusFixVersion(getBugKey(i)))
                print("]")


def addBugKeyToArrIssue():
    for i in ParsXMLPickTestKeyFail():
        credentials.ISSUE.append(getBugKey(i))


def main():
    parser = argparse.ArgumentParser(description='Creates a demo Xray project in a Jira Software cloud instance.')
    parser.add_argument('-s', '--salt', action='store_true',
                        help='appends 3 random chars to the project name (useful if you already have a project with '
                             'the same name or key)')
    parser.add_argument('-v', '--verbose', action='store_true', help='enables verbose logging')

    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=(logging.INFO if args.verbose == False else logging.DEBUG))

    try:
        os.system(credentials.RUN_TEST_CASES)
    except:
        print('could not execute command Robot')

    try:
        scope = Scope()
        infoProject(scope)
        xrayApi = setup(scope)
        with open(credentials.PATH_OUTPUT_ROBOT_FRAMEWORK) as data_file:
            data = data_file.read()
            print('[ Import Test Execution Key ' + credentials.TEST_EXECUTION_KEY + ' ]')
            xrayApi.importRobotResults(data)
            checkAndCreateBug(scope)
        print("[ Sprint Id ")
        print(getSprintIdOfBoard())
        print(" ]")
        print("[ Key of bug : ")
        addBugKeyToArrIssue()
        print(credentials.ISSUE)
        print("]")
        log.info('[ Added bug to ' + credentials.SPRINT + " ]")
        jira.addIssueToSprint(getSprintIdOfBoard())
        log.info(f'All Done. Please check project with key {scope.projectKey}.')
        log.info('Enjoy. Bye!')
    except HTTPError as e:
        log.error(f'HTTP Error {e.response.status_code}: {e.response.text}')
        exit(2)


if __name__ == '__main__':
    main()
