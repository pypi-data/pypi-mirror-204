# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evaluateqa', 'evaluateqa.mintaka']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0', 'pandas>=2.0.1,<3.0.0', 'ujson>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'evaluateqa',
    'version': '0.1.0',
    'description': '',
    'long_description': "[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# EvaluateQA\n\nPackage for evaluate QA datasets and Leaderboard with SOTA approaches\n\n## Install\n\n```bash\npip install evaluateqa\n```\n\n## Supported datasets\n\n\n### [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://github.com/amazon-science/mintaka)\n\n```python\nfrom evaluateqa.mintaka import evaluate\n\npredictions = {\n    '9ace9041': 'Q90',\n    '9ace9042': 3,\n    ...\n}\n\nresults = evaluate(\n    predictions,\n    split='test',\n    mode='kg',\n    lang='en',\n)\n```\n\n\n\n",
    'author': 'Mikhail Salnikov',
    'author_email': '2613180+MihailSalnikov@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
