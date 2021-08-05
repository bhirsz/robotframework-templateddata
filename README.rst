.. Badges

|License|

TemplatedData
=============
.. contents::
   :local:

Introduction
------------
TemplatedData is Robot Framework library for dynamically generated test data using robot variables and Jinja templating.

Requirements
------------
Python 3.6+ and Robot Framework 3.2.1+.

TemplatedData will most likely work on other versions but it's not tested on them.

Installation
------------
You can install TemplateData by running::

    pip install robotframework-templateddata

Usage
--------
You need to import TemplatedData as library first::

    *** Settings ***
    Library    TemplatedData

TemplatedData will replace all occurences of robot variables (${var}) in file or variable using current robot context
and scopes. All test data in below examples are saved under 'test_data.txt' files

Test data::

    my variable is ${var}

Robot code::

    ${var}     Set Variable    ${10}
    ${data}    Get Templated Data From Path    test_data.txt
    Log    ${data} # it should print `my variable is 10`

If the variable is not found it will be replaced with empty string. You can override that behaviour::

    ${data}    Get Templated Data From Path    test_data.txt    default_empty=${5}
    Log    ${data} # it should print `my variable is 5`

You can also set default value of variable with `:` symbol.

Test data::

    my variable is ${var} and ${var2:some string}

Robot code::

    ${var}     Set Variable    ${10}
    ${data}    Get Templated Data From Path    test_data.txt
    Log    ${data} # it should print `my variable is 10 and some string`

Return value can be either text/string (default) or json.

Test data::

    { "key": "${var}" }

Robot code::

    ${data}    Get Templated Data From Path    test_data.txt    var=value    return_type=json
    Log    ${data} # it should print `{ "key": "value" }` and ${data} will be of type json
   
.. Badges links

.. |License|
   image:: https://img.shields.io/pypi/l/robotframework-robocop
   :alt: PyPI - License
