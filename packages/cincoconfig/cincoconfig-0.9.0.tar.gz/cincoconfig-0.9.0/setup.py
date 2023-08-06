# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cincoconfig', 'cincoconfig.fields', 'cincoconfig.formats']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cincoconfig',
    'version': '0.9.0',
    'description': 'Universal configuration file parser',
    'long_description': '# Cinco Config\n\n[![Build Status](https://travis-ci.com/ameily/cincoconfig.svg?branch=master)](https://travis-ci.com/github/ameily/cincoconfig)\n[![Coverage Status](https://coveralls.io/repos/github/ameily/cincoconfig/badge.svg?branch=master)](https://coveralls.io/github/ameily/cincoconfig?branch=master)\n[![Docs Status](https://readthedocs.org/projects/cincoconfig/badge/)](https://cincoconfig.readthedocs.io/en/latest/)\n\nNext generation universal configuration file parser. The config file structure is defined\nprogrammatically and expressively, no need to create classes and inheritance.\n\nLet\'s get right to it:\n\n```python\n# app_config.py\nimport getpass\nfrom cincoconfig import *\n\n# first, define the configuration\'s schema -- the fields available that\n# customize the application\'s or library\'s behavior\nschema = Schema()\nschema.mode = ApplicationModeField(default=\'production\')\n\n# nested configurations are built on the fly\n# http is now a subconfig\nschema.http.port = PortField(default=8080, required=True)\n\n# each field has its own validation rules that are run anytime the config\n# value is loaded from disk or modified by the user.\n# here, this field only accepts IPv4 network addresses and the user is\n# required to define this field in the configuration file.\nschema.http.address = IPv4AddressField(default=\'127.0.0.1\', required=True)\n\nschema.http.ssl.enabled = BoolField(default=False)\nschema.http.ssl.cafile = FilenameField()\nschema.http.ssl.keyfile = FilenameField()\nschema.http.ssl.certfile = FilenameField()\n\nschema.db.host = HostnameField(allow_ipv4=True, required=True, default=\'localhost\')\nschema.db.port = PortField(default=27017, required=True)\nschema.db.name = StringField(default=\'my_app\', required=True)\nschema.db.user = StringField(default=\'admin\')\n\n# some configuration values are sensitive, such as credentials, so\n# cincoconfig provides config value encryption when the value is\n# saved to disk via the SecureField\nschema.db.password = SecureField()\n\n# get a field programmatically\nprint(schema[\'db.host\']) # >>> schema.db.host\n\n# once a schema is defined, build the actual configuration object\n# that can load config files from disk and interact with the values\nconfig = schema()\n\n# print the http port\nprint(config.http.port) # >>> 8080\n\n# print the http port programmatically\nprint(config[\'http.port\']) # >>> 8080\n\nconfig.db.password = getpass.getpass("Enter Password: ") # < \'password\'\n\n# set a config value manually\nif config.mode == \'production\':\n    config.db.name = config.db.name + \'_production\'\n\nprint(config.dumps(format=\'json\', pretty=True).decode())\n# {\n#   "mode": "production",\n#   "http": {\n#     "port": 8080,\n#     "address": "127.0.0.1"\n#     "ssl": {\n#       "enabled": false\n#     }\n#   },\n#   "db": {\n#     "host": "localhost",\n#     "port": 27017,\n#     "name": "my_app_production",\n#     "user": "admin",\n#     "password": {\n#       "method": "best",\n#       "ciphertext": "<ciphertext>"\n#     }\n#   }\n# }\n```\n\n### Override Configuration with Command Line Arguments (argparse)\n\n```python\n# config.py\nschema = Schema()\nschema.mode = ApplicationModeField(default=\'production\', modes=[\'production\', \'debug\'])\nschema.http.port = PortField(default=8080, required=True)\nschema.http.address = IPv4AddressField(default=\'127.0.0.1\', required=True)\n\nconfig = schema()\n\n# __main__.py\nimport argparse\nfrom .config import config, schema\n\nparser = schema.generate_argparse_parser()\n#\n# The generate_argparse_parser() method auto generates the parser using --long-opts. For this\n# configuration, the returned parser is equivalent to:\n#\n# parser = argparse.ArgumentParser()\n#\n# parser.add_argument(\'--http-address\', action=\'store\', dest=\'http.address\')\n# parser.add_argument(\'--http-port\', action=\'store\', dest=\'http.port\')\n# parser.add_argument(\'--mode\', action=\'store\', dest=\'mode\')\n#\n\n# new args can be added to the parser\nparser.add_argument(\'-c\', \'--config\', action=\'store\')\nargs = parser.parse_args()\nif args.config:\n    config.load(args.config, format=\'json\')\n\n# update the configuration with arguments specified via the command line\nconfig.cmdline_args_override(args, ignore=[\'config\'])\n```\n',
    'author': 'Adam Meily',
    'author_email': 'meily.adam@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ameily/cincoconfig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
