import re
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from jinja2 import Environment, BaseLoader


class TemplatedData:
    def __init__(self):
        self.built_in = BuiltIn()
        self.robot_var_pattern = re.compile(r'\${[^}]+}')

    @staticmethod
    def normalize(value):
        return value.lower()

    def get_templated_data(self, template, default_empty='', jinja_template=False, **kwargs):
        logger.debug('Template:')
        logger.debug(template)
        vars = self.robot_var_pattern.findall(template)
        overwrite_values = {arg: self.normalize(value) for arg, value in kwargs.items()}
        templated_vars = {}
        for var in vars:
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
        logger.debug('Rendered template:')
        logger.debug(replaced_data)
        return replaced_data

    def get_templated_data_from_path(self, path, default_empty='', jinja_template=False, **kwargs):
        with open(path) as f:
            template = f.read()
        return self.get_templated_data(template, default_empty, jinja_template, **kwargs)
