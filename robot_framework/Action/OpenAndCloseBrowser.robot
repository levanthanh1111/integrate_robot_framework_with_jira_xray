*** Settings ***
Resource  ../Config/ConfigBrowser.robot
*** Keywords ***
Start TestCase
    Open Browser    ${url}  ${browser}
    Maximize Browser Window
Finish TestCase
    Close Browser