# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['testapp_winstonyym']

package_data = \
{'': ['*'], 'testapp_winstonyym': ['data/*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0', 'pandas>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'testapp-winstonyym',
    'version': '0.1.0',
    'description': 'UAL Workshop demo',
    'long_description': '# testapp_winstonyym\n\nUAL Workshop demo\n\n## Installation\n\n```bash\n$ pip install testapp_winstonyym\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`testapp_winstonyym` was created by winstonyym. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`testapp_winstonyym` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'winstonyym',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
