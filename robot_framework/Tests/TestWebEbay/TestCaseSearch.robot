*** Settings ***
Resource  ../../Action/OpenAndCloseBrowser.robot
Resource  ../../Action/Search.robot
Resource  ../../Action/SearchResult.robot

Test Setup  Start TestCase
Test Teardown  Finish TestCase

*** Test Cases ***
Test Search Five
    [Documentation]  This test five
    [Tags]  DRJ-12
    Input Search Text and Click Search   mobile
    Verify Search Results       laptop

*** Test Cases ***
Test Search Seven
    [Documentation]  This test seven
    [Tags]  DRJ-13
    Input Search Text and Click Search   @@!!
    Verify Search Results       @@!!
