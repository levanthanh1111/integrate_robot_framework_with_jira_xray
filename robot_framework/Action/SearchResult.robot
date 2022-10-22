*** Settings ***
Resource  ../CommonFunctionality/TemporaryData/WebEbay/DataSearch.robot
*** Keywords ***
Verify Search Results
    [Arguments]  ${name}
    Page Should Contain    results for ${name}