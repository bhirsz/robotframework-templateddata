*** Settings ***
Library     OperatingSystem


*** Variables ***
${SOURCE_DIR}    ${CURDIR}${/}test_data${/}


*** Keywords ***
Template Should Render Correctly
    [Arguments]    ${actual}    ${expected_path}
    ${expected}    Get File    ${expected_path}
    Should Be Equal    ${actual}    ${expected}
