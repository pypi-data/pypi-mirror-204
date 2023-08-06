# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gluetool', 'gluetool.pylint', 'gluetool.tests']

package_data = \
{'': ['*'],
 'gluetool.tests': ['assets/parse_config/configroot/config/*',
                    'assets/parse_config/configroota/config/*',
                    'assets/parse_config/configrootb/config/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'MarkupSafe>=2.0.0,<3.0.0',
 'Sphinx>=5.0.0,<6.0.0',
 'attrs>=22.2.0,<23.0.0',
 'beautifulsoup4',
 'cattrs>=22.2.0,<23.0.0',
 'colorama',
 'configparser',
 'docutils',
 'lxml',
 'mock',
 'mypy-extensions',
 'packaging',
 'raven',
 'requests',
 'requests-toolbelt',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'six',
 'tabulate',
 'urlnormalizer',
 'zipp']

entry_points = \
{'console_scripts': ['gluetool = gluetool.tool:main',
                     'gluetool-html-log = gluetool.html_log:main'],
 'gluetool.modules': ['.bash_completion = '
                      'gluetool_modules.bash_completion:BashCompletion',
                      '.dep_list = gluetool_modules.dep_list:DepList',
                      '.yaml_pipeline = '
                      'gluetool_modules.yaml_pipeline:YAMLPipeline']}

setup_kwargs = {
    'name': 'gluetool',
    'version': '2.4',
    'description': 'Python framework for constructing command-line pipelines.',
    'long_description': 'gluetool - A tool for gluing together one-file python modules in a sequential command-line pipeline\n---------------------------------------------------------------------------------------------------\n\n``gluetool`` is a command line centric generic framework useable for glueing modules into pipeline\n\n\n.. image:: https://travis-ci.org/gluetool/gluetool.svg?branch=master\n    :target: https://travis-ci.org/gluetool/gluetool\n\n.. image:: https://codecov.io/gh/gluetool/gluetool/branch/master/graph/badge.svg\n     :target: https://codecov.io/gh/gluetool/gluetool\n     :alt: Code coverage\n\n.. image:: https://requires.io/github/gluetool/gluetool/requirements.svg?branch=master\n     :target: https://requires.io/github/gluetool/gluetool/requirements/?branch=master\n     :alt: Requirements Status\n\n.. image:: https://readthedocs.org/projects/gluetool/badge/?version=latest\n     :target: http://gluetool.readthedocs.io/en/latest/?badge=latest\n     :alt: Documentation Status\n\n\nDocumentation\n-------------\n\nFor more information see documentation:\n\nhttp://gluetool.readthedocs.io/\n',
    'author': 'Milos Prchlik',
    'author_email': 'mprchlik@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gluetool.readthedocs.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<3.10',
}


setup(**setup_kwargs)
