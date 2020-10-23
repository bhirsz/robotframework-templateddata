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
        overwrite_values = {arg: self.normalize(value) for arg, value in kwargs.items()}
        templated_vars = {}
        for var in self.robot_var_pattern.findall(template):
            name, *default = var[2:-1].split(':', maxsplit=1)
            default = default[0] if default else default_empty
            raw_name, *attrs = name.split('.', maxsplit=1)
            default = self.built_in.get_variable_value(f'${{{raw_name}}}', default)
            default = overwrite_values.get(raw_name, default)
            templated_vars[raw_name] = default
            if jinja_template:
                var_replaced = f'templated_vars["{raw_name}"]'
                if attrs:
                    var_replaced += '.' + attrs[0]
            else:
                var_replaced = str(default)
            template = template.replace(var, var_replaced)
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
