import re
import json
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from jinja2 import Environment, BaseLoader


class TemplatedData:
    def __init__(self, default_empty='', jinja_template=False, return_type='text'):
        self.default_empty = default_empty
        self.jinja_template = jinja_template
        self.return_type = return_type
        self.built_in = BuiltIn()
        self.robot_var_pattern = re.compile(r'\${[^}]+}')

    @staticmethod
    def normalize(value):
        return value.lower()

    def get_templated_data(self, template, **kwargs):
        default_empty = kwargs.pop('default_empty', self.default_empty)
        jinja_template = kwargs.pop('jinja_template', self.jinja_template)
        return_type = kwargs.pop('return_type', self.return_type)
        logger.debug(f'Template:\n{template}')
        overwrite_values = {self.normalize(arg): value for arg, value in kwargs.items()}
        templated_vars = {}
        elements = _search_variables(template, default_empty)
        template = resolve(elements, overwrite_values, jinja_template, templated_vars)
        if jinja_template:
            r_template = Environment(loader=BaseLoader()).from_string(template)
            replaced_data = r_template.render(templated_vars=templated_vars)
        else:
            replaced_data = template
        logger.debug(f'Rendered template:\n{replaced_data}')
        return self.return_data_with_type(replaced_data, return_type)

    def get_templated_data_from_path(self, path, **kwargs):
        with open(path) as f:
            template = f.read()
        return self.get_templated_data(template, **kwargs)

    @staticmethod
    def return_data_with_type(data, data_type):
        if data_type == 'json':
            return json.loads(data)
        return data


class Variable:
    def __init__(self, string, default_empty):
        elements = _search_variables(string, default_empty)

        for index, elem in enumerate(elements):
            if isinstance(elem, str):
                if ':' in elem:
                    pre, suf = elem.split(':', maxsplit=1)
                    self.value = elements[:index]
                    self.default = elements[index+1:]
                    if pre:
                        self.value.append(pre)
                    if suf:
                        self.default.insert(0, suf)
                    break
        else:
            self.value = elements
            self.default = default_empty

    def resolve(self, overwrite_values, jinja_template, templated_vars):
        value = resolve(self.value, overwrite_values, jinja_template, templated_vars)
        raw_name, *attrs = value.split('.', maxsplit=1)
        if raw_name in overwrite_values:
            default = overwrite_values[raw_name]
        else:
            default = BuiltIn().get_variable_value(f'${{{raw_name}}}', resolve(self.default, overwrite_values, jinja_template, templated_vars))

        templated_vars[raw_name] = default
        if jinja_template:
            var_replaced = f'templated_vars["{raw_name}"]'
            if attrs:
                var_replaced += '.' + attrs[0]
        else:
            var_replaced = str(default)
        return var_replaced


def resolve(elements, overwrite_values, jinja_template, templated_vars):
    new_elements = []
    for elem in elements:
        if isinstance(elem, Variable):
            elem = elem.resolve(overwrite_values, jinja_template, templated_vars)
        new_elements.append(elem)
    return ''.join(new_elements)


def _search_variables(string, default_empty):
    """ return list in form of [string, Variable, string, Variable.. ] .
        Following string: "my value is ${value}." will return: ["my value is", Variable("${value}"), .]
    """
    elements = []
    if not string:
        return elements
    while True:
        var_start = string.find('${')
        if var_start < 0:
            if string:
                elements.append(string)
            break
        if var_start:
            elements.append(string[:var_start])
        string = string[var_start+2:]
        bracket = 1
        for index, char in enumerate(string):
            if char == '{':
                bracket += 1
            elif char == '}':
                bracket -= 1
            if not bracket:
                elements.append(Variable(string[:index], default_empty))
                string = string[index+1:]
                break
        else:
            if string:
                elements.append(string)
            break
    return elements
