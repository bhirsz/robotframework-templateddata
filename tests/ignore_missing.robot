*** Settings ***
Library    TemplatedData    ignore_missing=True

Resource    resource.resource


*** Variables ***
${TEMPLATE_PATH}           ${SOURCE_DIR}ignore_missing${/}templated_data.json
${JINJA_TEMPLATE_PATH}     ${SOURCE_DIR}ignore_missing${/}jinja.json


*** Test Cases ***
Get templated data and ignore not existing
    ${robot_variable}    Set Variable    VALUE
    ${template}    Get File    ${TEMPLATE_PATH}
    ${data}    Get Templated Data    ${template}
    Template Should Render Correctly    ${data}    ${SOURCE_DIR}ignore_missing${/}not_replaced.json
    Log    ${data}

Get templated data and do not ignore not existing
    ${robot_variable}    Set Variable    VALUE
    ${template}    Get File    ${TEMPLATE_PATH}
    ${data}    Get Templated Data    ${template}    ignore_missing=False
    Template Should Render Correctly    ${data}    ${SOURCE_DIR}ignore_missing${/}replaced.json
    Log    ${data}

Get templated data with jinja and ignore not existing
    ${robot_variable}    Set Variable    VALUE
    ${template}    Get File    ${JINJA_TEMPLATE_PATH}
    ${data}    Get Templated Data    ${template}    jinja_template=${True}
    Template Should Render Correctly    ${data}    ${SOURCE_DIR}ignore_missing${/}jinja_after.json
    Log    ${data}
