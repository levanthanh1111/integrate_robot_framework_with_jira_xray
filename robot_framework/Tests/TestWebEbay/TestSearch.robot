*** Settings ***
Resource  ../../Action/OpenAndCloseBrowser.robot
Resource  ../../Action/Search.robot
Resource  ../../Action/SearchResult.robot

Test Setup  Start TestCase
Test Teardown  Finish TestCase


*** Test Cases ***
Test Search Four
    [Documentation]  This test four
    [Tags]  DRJ-11
    Input Search Text and Click Search   robot
    Verify Search Results       robot


Test Search Five
    [Documentation]  This test five
    [Tags]  DRJ-12
    Input Search Text and Click Search   mobile
    Verify Search Results       laptop

Test Search Six
    [Documentation]  This test six
    [Tags]  DRJ-13
    Input Search Text and Click Search   mobile
    Verify Search Results       mobile
