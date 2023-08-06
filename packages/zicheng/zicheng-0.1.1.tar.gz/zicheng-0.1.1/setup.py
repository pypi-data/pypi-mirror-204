# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zicheng']

package_data = \
{'': ['*'], 'zicheng': ['data/*']}

setup_kwargs = {
    'name': 'zicheng',
    'version': '0.1.1',
    'description': 'zicheng',
    'long_description': '# zicheng\n\nzicheng\n\n## Installation\n\n```bash\n$ pip install zicheng\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`zicheng` was created by zicheng. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`zicheng` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'zicheng',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
