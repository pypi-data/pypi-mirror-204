# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_experimenter']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'jupyterlab>=3.5.0,<4.0.0',
 'mysql-connector-python>=8.0',
 'numpy>=1.15',
 'pandas>=1.0']

setup_kwargs = {
    'name': 'py-experimenter',
    'version': '1.2.1',
    'description': 'The PyExperimenter is a tool for the automatic execution of experiments, e.g. for machine learning (ML), capturing corresponding results in a unified manner in a database.',
    'long_description': '[![Project Homepage](https://img.shields.io/badge/Project%20Homepage-tornede.github.io/py_experimenter-0092CD)](https://tornede.github.io/py_experimenter)\n[![Pypi](https://img.shields.io/pypi/v/py_experimenter)](https://pypi.org/project/py-experimenter/)\n[![License](https://img.shields.io/github/license/tornede/py_experimenter)](https://tornede.github.io/py_experimenter/license.html)\n[![DOI](https://joss.theoj.org/papers/10.21105/joss.05149/status.svg)](https://doi.org/10.21105/joss.05149)\n\n![Tests](https://github.com/tornede/py_experimenter/actions/workflows/tests.yml/badge.svg)\n![GitHub Pages](https://github.com/tornede/py_experimenter/actions/workflows/github-pages.yml/badge.svg)\n\n<img src="docs/source/_static/py-experimenter-logo.png" alt="PyExperimenter Logo: Python biting a database" width="200px"/>\n\n# PyExperimenter\n\n`PyExperimenter` is a tool to facilitate the setup, documentation, execution, and subsequent evaluation of results from an empirical study of algorithms and in particular is designed to reduce the involved manual effort significantly.\nIt is intended to be used by researchers in the field of artificial intelligence, but is not limited to those.\n\nThe empirical analysis of algorithms is often accompanied by the execution of algorithms for different inputs and variants of the algorithms (specified via parameters) and the measurement of non-functional properties.\nSince the individual evaluations are usually independent, the evaluation can be performed in a distributed manner on an HPC system.\nHowever, setting up, documenting, and evaluating the results of such a study is often file-based.\nUsually, this requires extensive manual work to create configuration files for the inputs or to read and aggregate measured results from a report file.\nIn addition, monitoring and restarting individual executions is tedious and time-consuming.\n\nThese challenges are addressed by `PyExperimenter` by means of a single well defined configuration file and a central database for managing massively parallel evaluations, as well as collecting and aggregating their results.\nThereby, `PyExperimenter` alleviates the aforementioned overhead and allows experiment executions to be defined and monitored with ease.\n\n![General schema of `PyExperimenter`.](docs/source/_static/workflow.png)\n\nFor more details check out the [`PyExperimenter` documentation](https://tornede.github.io/py_experimenter/):\n\n- [Installation](https://tornede.github.io/py_experimenter/installation.html)\n- [Examples](https://tornede.github.io/py_experimenter/examples/example_general_usage.html)\n\n## Cite PyExperimenter\n\nIf you use `PyExperimenter` in a scientific publication, we would appreciate a citation in one of the following ways.\n\n### Citation String\n\nTornede et al., (2023). PyExperimenter: Easily distribute experiments and track results. Journal of Open Source Software, 8(84), 5149, https://doi.org/10.21105/joss.05149\n\n### BibTex\n```\n@article{Tornede2023, \n    title = {{PyExperimenter}: Easily distribute experiments and track results}, \n    author = {Tanja Tornede and Alexander Tornede and Lukas Fehring and Lukas Gehring and Helena Graf and Jonas Hanselle and Felix Mohr and Marcel Wever}, \n    journal = {Journal of Open Source Software},\n    publisher = {The Open Journal},  \n    year = {2023}, \n    volume = {8}, \n    number = {84}, \n    pages = {5149}, \n    doi = {10.21105/joss.05149}, \n    url = {https://doi.org/10.21105/joss.05149}\n}\n```\n',
    'author': 'Tanja Tornede',
    'author_email': 't.tornede@ai.uni-hannover.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tornede/py_experimenter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
