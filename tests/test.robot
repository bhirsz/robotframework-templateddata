*** Settings ***
Library    OperatingSystem
Library    TemplatedData  jinja_template=${True}


*** Variables ***
${TEMPLATE_PATH}           templated_data_jinja.json
${TEMPLATE_PATH_SIMPLE}    templated_data.json
&{USERS}    bartek=5    tymoteusz=10    pawel=-1


*** Test Cases ***
Get template itself
    ${template}    Get File    ${TEMPLATE_PATH}
    Log    ${template}

Get templated data without vars in scope
    ${data}    Get Templated Data From Path    ${TEMPLATE_PATH}    default_empty=THIS IS EMPTY
    Log    ${data}

Get templated data with one local var in scope
    ${account_id2}    Set Variable    ${10}
    ${data}    Get Templated Data From Path    ${TEMPLATE_PATH}
    Log    ${data}

Get templated data with all var in scope
    ${account_id2}    Set Variable    ${10}
    ${account_id}     Set Variable    ${10}
    ${data}    Get Templated Data From Path    ${TEMPLATE_PATH}
    Log    ${data}

Get templated data without jinja
    ${account_id2}    Set Variable    ${10}
    ${account_id}     Set Variable    ${10}
    ${data}    Get Templated Data From Path    ${TEMPLATE_PATH_SIMPLE}    jinja_template=${False}
    Log    ${data}

Get templated data with return type json
    ${account_id2}    Set Variable    ${10}
    ${account_id}     Set Variable    ${10}
    ${data}    Get Templated Data From Path    ${TEMPLATE_PATH}    return_type=json
    Log    ${data}

Get templated data from variable
    ${account_id2}    Set Variable    ${10}
    ${account_id}     Set Variable    ${10}
    ${template}    Get File    ${TEMPLATE_PATH}
    ${data}    Get Templated Data    ${template}
    Log    ${data}
