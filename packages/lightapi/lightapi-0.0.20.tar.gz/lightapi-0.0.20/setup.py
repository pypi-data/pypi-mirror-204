# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lightapi']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0']

setup_kwargs = {
    'name': 'lightapi',
    'version': '0.0.20',
    'description': "Light API turns LLM's into Autonomous, MultiModal, MultiTasking Agents.",
    'long_description': '<h1 align=left><strong>Light API 0.0.19</strong></h1>\n\n<div align=left>\n <a href="https://github.com/Aeternalis-Ingenium/FastAPI-Backend-Template/actions/workflows/ci-backend.yaml">\n  <img src="https://github.com/Aeternalis-Ingenium/FastAPI-Backend-Template/actions/workflows/ci-backend.yaml/badge.svg"/> \n </a>\n\n <a href="https://codecov.io/gh/Aeternalis-Ingenium/FastAPI-Backend-Template">\n  <img src="https://codecov.io/gh/Aeternalis-Ingenium/FastAPI-Backend-Template/branch/trunk/graph/badge.svg?token=1hiVayuLRl"/> \n </a>\n\n <a href="https://github.com/pre-commit/pre-commit">\n  <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="pre-commit" style="max-width:100%;">\n </a>\n\n <a href="https://github.com/psf/black">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg">\n </a>\n\n <a href="https://pycqa.github.io/isort/">\n  <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336">\n </a>\n\n <a href="http://www.mypy-lang.org/static/mypy_badge.svg">\n  <img src="https://camo.githubusercontent.com/59eab954a267c6e9ff1d80e8055de43a0ad771f5e1f3779aef99d111f20bee40/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667" alt="check with mypy" style="max-width:100%;">\n </a>\n<br>\n\n\n## Introduction\n\nLight Assistant powered by LightAI is an AI-powered application designed to help you streamline your work and free up time for more important tasks. It can handle a wide range of tasks, from organizing files to managing your email inbox, scheduling meetings, and much more.\n\n## Installation\n\n`pip install lightapi`\n\n## Authentication\n\nTo use the LightAI Assistant API, you will need to create an account and generate an API key. You can do this by visiting the [Light API](https://beta.lightapi.com) website.\n\n## Usage\n\n```\nimport lightapi\n\nclient = lightapi.LightClient("YOUR_API_KEY_HERE")\n\n```\n## Documentation\n\nFor a comprehensive understanding of LightAI Assistant\'s features and capabilities, visit our [Documentation](https://docs.lightapi.com).\n',
    'author': 'Jordan Plows ',
    'author_email': 'jordan@lightapi.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
