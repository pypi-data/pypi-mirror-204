# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvg_api', 'mvg_api.api', 'mvg_api.models', 'mvg_api.tests']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.3.0,<24.0.0',
 'httpx>=0.24.0,<0.25.0',
 'levenshtein>=0.21.0,<0.22.0',
 'pydantic>=1.10.7,<2.0.0',
 'pylint>=2.15.7,<3.0.0',
 'pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'async-mvg-api',
    'version': '0.1.4',
    'description': '',
    'long_description': '# Unofficial MVG api\n\nAn async and sync wrapper for the MVG endpoints, with data validation over pydantic\n\n# Usage policy of the MVG api\n## ACHTUNG: \nUnsere Systeme dienen der direkten Kundeninteraktion. Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar. Wir behalten uns vor, die Duldung grundsätzlich oder in Einzelfällen zu widerrufen. Fragen richten Sie bitte gerne an: redaktion@mvg.de.\n\nIn other words: Private, noncomercial, moderate use of the API is tolerated. They don\'t consider data mining as moderate use.\n\n(Disclaimer: I am not a lawyer, this isn\'t legal advice)\n\n## Installation\npip installation or clone the repository and install the [poetry](https://python-poetry.org/) dependencies\n\n```bash\npip install async-mvg-api\n```\n\nor \n\n```bash\ngit clone https://github.com/Plutokekz/MVG-Api.git\ncd MVG-Api\npoetry install\n```\n## Usage\n\n```python\nfrom mvg_api.mvg import MVG\nmvg = MVG()\nmvg.get_location("Hauptbahnhof")\n```\n\n## Tests\n\n```bash\npoetry run pytest mvg_api/tests/api_tests.py\n```\n\n# Credit\nFor Endpoint Information and Code snippets\n* https://github.com/leftshift/python_mvg_api\n* https://www.mvg.de/\n',
    'author': 'Lukas Mahr',
    'author_email': 'lukas@yousuckatprogramming.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
