# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfsjson', 'dfsjson.src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dfsjson',
    'version': '1.0.11',
    'description': 'A robust JSON encoder that fixes errors by utilizing DFS algorithm.',
    'long_description': '# DFS JSON\nA Depth First Search powered JSON encoding library. For the remaining operations (dump, dumps), it uses standard python JSON library.\n\n# Installation\n```\npip install dfsjson\n```\n\n# Usage\n\n```\n# Create a complex JSON object\nexample_json = """{\n    "key1": "value1\'\n    "key2": [1 2, 3]\n    "key3":  {\n        "subkey1": "subvalue1"\n        "subkey2": "subvalue2"\n    ,\n}"""\n\ndj = DFSJson(max_depth = 100, max_diff = 10)\ndj.loads(example_json)\n\n```\n\n# Discussion\n### Hey I know this. Why not have you used Breadth First Search?\nTechnically you are correct but keep in mind that Breadth First Search keeps the previous states in its list which \nscales with number of iterations you are making and it can be a huge strain on the memory.\n\nHowever, Depth First search requires only O(log(n)) memory complexity in which we can search a lot more possibilities.\n\n# Contribution\nPlease don\'t hesitate to create issues and pull requests since this is developed overnight.',
    'author': 'Unsal Gokdag',
    'author_email': 'unsal.gokdag@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AutomaticHourglass/dfsjson',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
