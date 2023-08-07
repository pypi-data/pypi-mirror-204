# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_datepicker']

package_data = \
{'': ['*']}

install_requires = \
['pendulum', 'textual>=0.14.0']

setup_kwargs = {
    'name': 'textual-datepicker',
    'version': '0.2.4',
    'description': 'A datepicker widget for Textual.',
    'long_description': '# Textual: DatePicker\n\nA DatePicker widget for [textual](https://github.com/Textualize/textual). It can be used standalone or with a DateSelect opening the dialog.\n\nDateSelect with DatePicker example:\n\n![DateSelect with DatePicker](https://user-images.githubusercontent.com/922559/209947716-3ee53f74-4d98-4d9c-a261-afb84955d519.png)\n\n\n## Usage\n\n```python\nfrom textual_datepicker import DateSelect\n\nDateSelect(\n  placeholder="please select",\n  format="YYYY-MM-DD",\n  picker_mount="#main_container"\n)\n```\n\nDefine an initial value:\n\n```python\nimport pendulum\nfrom textual_datepicker import DateSelect\n\nDateSelect(\n  placeholder="please select",\n  format="YYYY-MM-DD",\n  date=pendulum.parse("2023-02-14"),\n  picker_mount="#main_container"\n)\n```\n\n## Installation\n\n```bash\npip install textual-datepicker\n```\n\nRequires textual 0.6.0 or later.\n\n## Limitations\n\nThis textual widget is in early stage and has some limitations:\n\n* It can only open below, not above: Make sure to reserve space below for the dialog.\n* It needs a specific mount point (`picker_mount`) where the dialog\n  shall appear. This is needed because the container widget with the select\n  itself could be too small. Maybe in future versions this will no longer be\n  needed.\n',
    'author': 'Mischa Schindowski',
    'author_email': 'mschindowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mitosch/textual-datepicker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
