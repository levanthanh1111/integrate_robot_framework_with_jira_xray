*** Settings ***
Resource  ../CommonFunctionality/Locator/WebEbay/HomePage.robot
Resource  ../CommonFunctionality/TemporaryData/WebEbay/DataSearch.robot
*** Keywords ***
Input Search Text and Click Search
#   step 1 : type key 'aa' into textSearch
#   Step 2 : click oh in
    [Arguments]  ${name}
    Input Text  ${textSearch}   ${name}
    Click Button   ${btnSearch}
