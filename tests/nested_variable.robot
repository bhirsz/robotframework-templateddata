*** Settings ***
Library     OperatingSystem
Library     TemplatedData

Resource    resource.resource


*** Variables ***
${VARNAME}       VALUE


*** Test Cases ***
Nothing set
    [Template]    Nothing set
    nested_variable
    nested_variable2
    nested_variable3
    nested_variable4
    nested_variable5
    empty_default

Default set
    [Template]    Default set
    nested_variable
    nested_variable2
    nested_variable3
    nested_variable4
    nested_variable5

Default and variable set
    [Template]    Default and variable set
    nested_variable
    nested_variable2
    nested_variable3
    nested_variable4
    nested_variable5
    empty_default


*** Keywords ***
Nothing set
    [Arguments]    ${source}
    ${data}    Get Templated Data From Path    ${SOURCE_DIR}${source}.txt
    Template Should Render Correctly    ${data}    ${SOURCE_DIR}${source}_nothing.txt
    Log    ${data}

Default set
    [Arguments]    ${source}
    ${DEFAULT}    Set Variable    10
    ${data}    Get Templated Data From Path    ${SOURCE_DIR}${source}.txt
    Template Should Render Correctly    ${data}    ${SOURCE_DIR}${source}_default.txt
    Log    ${data}

Default and variable set
    [Arguments]    ${source}
    ${DEFAULT}    Set Variable    10
    ${VALUE}      Set Variable    a
    ${data}    Get Templated Data From Path    ${SOURCE_DIR}${source}.txt
    Template Should Render Correctly    ${data}    ${SOURCE_DIR}${source}_all.txt
    Log    ${data}
