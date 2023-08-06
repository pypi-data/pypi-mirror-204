# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.app', 'src.app.classes', 'src.app.data']

package_data = \
{'': ['*'],
 'src': ['client/*',
         'client/css/*',
         'client/font/*',
         'client/js/*',
         'client/js/components/*',
         'client/js/components/elements/*',
         'client/js/components/items/*',
         'client/js/components/popups/*',
         'client/js/lib/*',
         'client/js/plots/*',
         'client/js/workers/*',
         'client/static/*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['npm-cockpit = src.app.app:init']}

setup_kwargs = {
    'name': 'npm-cockpit',
    'version': '0.4.0',
    'description': 'Installable command-line tool with web interface which helps to track nodejs project dependencies state',
    'long_description': '# NPM-COCKPIT\n\nA user-friendly application for JavaScript developers to visualize the dependency tree of NPM packages and NodeJS applications. \n\nAllows to get statistical info about application dependencies tree state. Provides an interface for filtering and viewing information through convenient tables and diagrams.\n\n## Features\n\nVisual representation of the entire dependency tree of a project. With ability to look all the paths for a specific package. Dependency tree can be visualized as a tree or directed network chart\n\n![tree chart](https://chartexample.com/images/npm-cockpit/network.jpg)\n\nDetailed information about each package, including version, description, and related links.\n\n![packages list](https://chartexample.com/images/npm-cockpit/list.jpg)\n\nIdentify potential issues such as outdated, deprecated or vulnerable packages.\n\n![packages list](https://chartexample.com/images/npm-cockpit/deprecated.jpg)\n\n**AND MUCH MORE!**\n\n\n## Requirements\n\n### General\n- Terminal or command prompt access\n- Target application folder should contain node_modules folder with installed dependencies and package.json\n- Node.js and NPM installed\n\n### As NPM package\n- `python` command should be available\n\n## Usage\n\n### Command params\n\n`path` - a path to project folder with package.json and node_modules inside\n\n`port` - available local port to serve the app (default `8080`)\n\n### PIP\n`pip install npm-cockpit`\n\n`npm-cockpit [path] [port]`\n\n### NPM globally installed\n`npm install --global npm-cockpit`\n\n`npm-cockpit [path] [port]`\n\n### NPX\n`npx npm-cockpit [path] [port]`\n\n### NPM dependency in package\n`npm install npm-cockpit` and add the run script in the package json with proper params\n\n## Development\n- `git clone https://github.com/b0000ring/npm-cockpit.git`\n- `cd npm-cockpit`\n- `node index.js [path] [port]` or `python __main__.py [path] [port]`\n',
    'author': 'Alex Chirkin',
    'author_email': 'hello@alexchirkin.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
