# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uiuc_490_sp23',
 'uiuc_490_sp23.Constraints',
 'uiuc_490_sp23.Exceptions',
 'uiuc_490_sp23.LineSearch',
 'uiuc_490_sp23.Optimizers',
 'uiuc_490_sp23.Problem',
 'uiuc_490_sp23.assignment1',
 'uiuc_490_sp23.assignment2',
 'uiuc_490_sp23.assignment3']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0', 'numpy>=1.24.2,<2.0.0', 'scipy>=1.10.1,<2.0.0']

entry_points = \
{'console_scripts': ['assignment1 = assignment1:__main__',
                     'assignment2 = assignment2:__main__',
                     'assignment3 = assignment3:__main__']}

setup_kwargs = {
    'name': 'uiuc-490-sp23',
    'version': '0.1.3',
    'description': "Programming assignments for UIUC's ECE490: Introduction to Optimization course during Spring 2023",
    'long_description': "# ECE490\nRepo to collaborate within for UIUC's ECE490, Spring 2023\n\n## Installation\n### Installation from PyPI\nThis should be as simple as:\n```bash\npython -m pip install uiuc-490-sp23\n```\n### Installation from Source\nThis project uses [Poetry](https://python-poetry.org/) Install it via\n[their instructions](https://python-poetry.org/docs/#installing-with-the-official-installer)\nand run:\n```bash\npoetry install\n```\nfrom this directory (preferably from within a `venv`).\n\n## Executing\nOnce installed, individual assignments can be ran by:\n```bash\npython -m uiuc_490_sp23.assignment<n>\n```\nwhere `<n>` is the assignment number. These will have a CLI implemented using argparse; if you're not sure,\njust run the above with `--help` to get a full list of commands.\n\n\n## Assignments\n### Assignment 1: Gradient Descent\nThis solves a simple, randomly generated quadratic minimization problem using Gradient Descent. It does so using\nboth fixed step size, as well as an adaptive backtracking line search (Armijo's rule).\n\n### Assignment 2: Newton's Method and Projected Gradient Descent\nThis assignment does two things:\n- Implements Newton's method to solve a simple 2D cubic polynomial and plots a fractal displaying the resulting solution based on the starting point\n- Implements Projected gradient descent and uses it to solve a simple box constrained optimization problem\n\n### Assignment 3: Augmented Lagrangian\nThis assignment implements the augmented Lagrangian to solve an equality constrained quadratic problem.",
    'author': 'Eric Silk',
    'author_email': 'eric.silk@ericsilk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eric-silk/ECE490',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
