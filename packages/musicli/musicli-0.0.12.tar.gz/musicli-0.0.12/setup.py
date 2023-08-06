# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['musicli']

package_data = \
{'': ['*']}

install_requires = \
['pick>=2.2.0,<3.0.0',
 'pillow>=9.5.0,<10.0.0',
 'pylast>=5.1.0,<6.0.0',
 'rich>=13.3.4,<14.0.0']

entry_points = \
{'console_scripts': ['musicli = musicli.musicli:start']}

setup_kwargs = {
    'name': 'musicli',
    'version': '0.0.12',
    'description': 'Rate, review, and catalogue all your artists and albums from the command line',
    'long_description': "# musicli\n\n[![PyPI](https://img.shields.io/pypi/v/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)\n[![PyPI - License](https://img.shields.io/pypi/l/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n---\nmusicli is a powerful and user-friendly Python package that allows users to easily rate, review, and catalogue their favorite artists and albums from the command line. With intuitive search and selection features, users can quickly navigate their music library and rate each album on a 10-point scale. The package also offers the option to rate individual tracks and includes a variety of customization options to personalize the cataloguing experience. Whether you're a music aficionado or simply looking to organize your music library, musicli is the perfect tool for music lovers everywhere.\n\n**Documentation**: [https://HighnessAtharva.github.io/musicli](https://HighnessAtharva.github.io/musicli)\n\n**Source Code**: [https://github.com/HighnessAtharva/musicli](https://github.com/HighnessAtharva/musicli)\n\n**PyPI**: [https://pypi.org/project/musicli/](https://pypi.org/project/musicli/)\n\n---\n\nRate, review, and catalogue all your artists and albums from the command line\n\n## Installation\n\n```sh\npip install musicli\n```\n\nGet a Last.fm API key from [here](https://www.last.fm/api/account/create) and set it as an environment variable:\n\n```sh\nset LASTFM_API_KEY=<your_api_key>\nset LASTFM_API_SECRET=<your_api_secret>\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings of the public signatures of the source code. The documentation is updated and published as a [Github project page](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nPublishing the package via poetry\n\n```sh\n# adding dependencies\npoetry add <new_dependency>\n\n# bumping the version\npoetry version <new_version>\n\n# installing the package\npoetry install\n\n# locking the dependencies [optional]\npoetry lock\n\n# building the package\npoetry build\n\n# publishing the package [token is already set initially]\npoetry publish\n```\n\nTrigger the [Draft release workflow](https://github.com/HighnessAtharva/musicli/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/HighnessAtharva/musicli/releases) and publish it. When a release is published, it'll trigger [release](https://github.com/HighnessAtharva/musicli/blob/master/.github/workflows/release.yml) workflow which creates PyPI release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nThis project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.\n",
    'author': 'Atharva Shah',
    'author_email': 'highnessatharva@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://HighnessAtharva.github.io/musicli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
