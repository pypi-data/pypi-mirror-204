# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tessif_examples',
 'tessif_examples.basic',
 'tessif_examples.plausibility',
 'tessif_examples.scientific',
 'tessif_examples.specialized']

package_data = \
{'': ['*'], 'tessif_examples': ['data/load_profiles/*']}

install_requires = \
['numpy', 'pandas', 'tessif>=0.0.25']

setup_kwargs = {
    'name': 'tessif-examples',
    'version': '0.3.2',
    'description': 'Tessif Examples Library',
    'long_description': 'tessif-examples\n===============\n\n|PyPI| |Python Version| |License| |Status|\n\n|Stable Release| |Develop Release|\n\n|Read the Docs| |Tests| |Safety| |Pylinting| |Flake8 Linting| |Pre-Commit|\n\n|Codecov| |Codacy| |Codeclimate| |Scrutinizer|\n\n|pre-commit| |Black| |Pylint| |Flake8|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/tessif-examples.svg\n   :target: https://pypi.org/project/tessif-examples/\n   :alt: PyPI\n\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/tessif-examples\n   :target: https://pypi.org/project/tessif-examples\n   :alt: Python Version\n\n.. |License| image:: https://img.shields.io/pypi/l/tessif-examples\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n\n.. |Status| image:: https://img.shields.io/pypi/status/tessif-examples.svg\n   :target: https://pypi.org/project/tessif-examples/\n   :alt: Status\n\n.. |Stable Release| image:: https://github.com/tZ3ma/tessif-examples/workflows/Stable-PyPI-Release/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Stable-PyPI-Release\n   :alt: Stable PyPI Release Workflow Status\n\n.. |Develop Release| image:: https://github.com/tZ3ma/tessif-examples/workflows/Develop-TestPyPI-Release/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Develop-TestPyPI-Release\n   :alt: Develop TestPyPI Release Workflow Status\n\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/tessif-examples/latest.svg?label=Read%20the%20Docs\n   :target: https://tessif-examples.readthedocs.io/\n   :alt: Read the documentation at https://tessif-examples.readthedocs.io/\n\n.. |Tests| image:: https://github.com/tZ3ma/tessif-examples/workflows/Tests-and-Coverage/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Tests-and-Coverage\n   :alt: Tests Workflow Status\n\n.. |Safety| image:: https://github.com/tZ3ma/tessif-examples/workflows/Safety/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Safety\n   :alt: Safety Workflow Status\n\n.. |Pylinting| image:: https://github.com/tZ3ma/tessif-examples/workflows/Pylinting/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Pylinting\n   :alt: Pylint Workflow Status\n\n.. |Flake8 Linting| image:: https://github.com/tZ3ma/tessif-examples/workflows/Flake8-Linting/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Flake8-Linting\n   :alt: Flake8-Linting Workflow Status\n\n.. |Pre-Commit| image:: https://github.com/tZ3ma/tessif-examples/workflows/Pre-Commit/badge.svg\n   :target: https://github.com/tZ3ma/tessif-examples/actions?workflow=Pre-Commit\n   :alt: Pre-Commit Workflow Status\n\n.. |Codecov| image:: https://codecov.io/gh/tZ3ma/tessif-examples/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/tZ3ma/tessif-examples\n   :alt: Codecov\n\n.. |Codacy| image:: https://app.codacy.com/project/badge/Grade/b278433bb9224147a2e6231d783b62e4\n   :target: https://app.codacy.com/gh/tZ3ma/tessif-examples/dashboard\n   :alt: Codacy Code Quality Status\n\n.. |Codeclimate| image:: https://api.codeclimate.com/v1/badges/ff119252f0bb7f40aecb/maintainability\n   :target: https://codeclimate.com/github/tZ3ma/tessif-examples/maintainability\n   :alt: Maintainability\n\n.. |Scrutinizer| image:: https://scrutinizer-ci.com/g/tZ3ma/tessif-examples/badges/quality-score.png?b=main\n   :target: https://scrutinizer-ci.com/g/tZ3ma/tessif-examples/\n   :alt: Scrutinizer Code Quality\n\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n.. |Pylint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen\n   :target: https://github.com/PyCQA/pylint\n   :alt: Package uses pylint\n\n.. |Flake8| image:: https://img.shields.io/badge/linting-flake8-yellogreen\n   :target: https://github.com/pycqa/flake8\n   :alt: Package uses flake8\n\n\nTessif_ example library\n\nInstallation\n------------\n\nPlease see the `Installation Guide`_ (`Github Repo Link`_) for details.\n\n\nUsage\n-----\n\nPlease see the `Worklow Reference <Workflow-Guide_>`_ (`Github Repo Link`_) for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_ (`Github Repo Link`_).\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_ (`Github Repo Link`_),\n*tessif-examples* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\nCredits\n-------\n\nThis project was created using the `Mathias Ammon <tZ3ma>`_ tweaked version of the\nHypermodern-Python_ project foundation proposed by `Claudio Jolowicz <cj>`_.\n\n.. _Tessif: https://github.com/tZ3ma/tessif\n\n.. _Hypermodern-Python: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _cj: https://github.com/cjolowicz\n\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n\n.. _file an issue: https://github.com/tZ3ma/tessif-examples/issues\n.. _pip: https://pip.pypa.io/\n\n.. _tZ3ma: https://github.com/tZ3ma\n.. working on github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Installation Guide: docs/source/getting_started/installation.rst\n.. _Workflow-Guide: docs/source/developer_guide/workflows.rst\n\n.. _Github Repo Link: https://github.com/tZ3ma/tessif-examples\n',
    'author': 'Mathias Ammon',
    'author_email': 'tz3ma.coding@use.startmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tZ3ma/tessif_examples',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
