# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_nested_browsable', 'drf_nested_browsable.templatetags']

package_data = \
{'': ['*'], 'drf_nested_browsable': ['templates/*']}

install_requires = \
['django>=4.2,<5.0', 'djangorestframework>=3.14.0,<4.0.0']

setup_kwargs = {
    'name': 'drf-nested-browsable',
    'version': '0.1.2',
    'description': 'Writable nested serializers with forms for the Browsable API',
    'long_description': ":warning: Work In Progress :warning:\n\n# Writable Nested Serializers with Browsable API Forms\n\nThis plugin is intended to provide writable nested serializers (similar to [the recommended plugin from DRF documentation](https://github.com/beda-software/drf-nested-browsable.git)) that bring their own forms for the Browsable API renderer.\n\n## Try it out\n\nThis project's dependencies are managed using [`poetry`](https://python-poetry.org/)\n\n```bash\ngit clone https://github.com/pcouy/drf-nested-browsable\ncd drf-nested-browsable\npoetry install\ncd example\npython manage.py migrate\npython manage.py runserver\n```\n\nThe above commands will install the dependencies, run the DB migrations, and launch a development server of the example project that uses the provided serializers.\n\n## Current state of the project\n\n### Done\n\n* Ability to write to a reverse `ForeignKey` relationship using serializer `Meta` class\n* Dynamic form for `WritableNestedListSerializer` that allows adding and removing children from the Browsable API\n* Basic example\n\n### To do\n\n* Make the current example work :\n  * Do not show `parent` select list when showing forms as children of another form\n  * Show `details` (`HyperlinkedIdentityField`) when displayed as a child Serializer\n* Write documentation / Auto-generate it from the docstrings ([pdoc](https://pdoc.dev/) ?)\n* Write tests/specs\n",
    'author': 'Pierre Couy',
    'author_email': 'contact@pierre-couy.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pierre-couy.dev/projects/drf-nested-browsable.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
