# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gmn_python_api']

package_data = \
{'': ['*'], 'gmn_python_api': ['data_models/*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'click==8.0.4',
 'future>=0.18.3',
 'numpy>1.20.3',
 'pandas>=1.1.0,<=1.3.5',
 'requests>=2.21.0,<3.0.0',
 'types-requests>=2.27.8,<3.0.0',
 'werkzeug>=2.2.3']

entry_points = \
{'console_scripts': ['gmn-python-api = gmn_python_api.__main__:main']}

setup_kwargs = {
    'name': 'gmn-python-api',
    'version': '0.0.9',
    'description': 'GMN Python API',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/gmn-python-api)](https://pypi.org/project/gmn-python-api/)\n[![Status](https://img.shields.io/pypi/status/gmn-python-api)](https://pypi.org/project/gmn-python-api/)\n[![Python versions](https://img.shields.io/pypi/pyversions/gmn-python-api)](https://pypi.org/project/gmn-python-api/)\n[![License](https://img.shields.io/pypi/l/gmn-python-api)](https://pypi.org/project/gmn-python-api/)\n\n[![Read the Docs](https://img.shields.io/readthedocs/gmn-python-api)](https://gmn-python-api.readthedocs.io/en/latest/)\n[![Tests](https://github.com/rickybassom/gmn-python-api/workflows/Tests/badge.svg)](https://github.com/rickybassom/gmn-python-api/actions?query=workflow%3ATests+branch%3Amain)\n[![Codecov](https://codecov.io/gh/rickybassom/gmn-python-api/branch/main/graph/badge.svg)](https://codecov.io/gh/rickybassom/gmn-python-api)\n\n[![Demo on Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/rickybassom/74d2c99ebbd612b88861038a5b33e021/gmn_data_analysis_template.ipynb)\n\n# gmn-python-api\n\nThis library provides a Python API for accessing open \n[Global Meteor Network](https://globalmeteornetwork.org/) (GMN) meteor trajectory \n[data](https://globalmeteornetwork.org/data/). Global meteor data is generated using a \nnetwork of low-light cameras pointed towards the night sky. Meteor properties (radiants,\norbits, magnitudes and masses) are produced by the GMN and are available through this\nlibrary.\n\n![Screenshot of GMN data](docs/screenshot.png)\n\n[Demo on Google Colab](https://colab.research.google.com/gist/rickybassom/74d2c99ebbd612b88861038a5b33e021/gmn_data_analysis_template.ipynb)\n\n## Features\n\n- Listing available daily and monthly meteor trajectory files from the \n  [GMN Data Directory](https://globalmeteornetwork.org/data/traj_summary_data/).\n\n- Downloading specific CSV meteor trajectory data from the GMN Data Directory or GMN \n  REST API.\n\n- Functions for loading meteor trajectory data into [Pandas](https://pandas.pydata.org/)\n  DataFrames.\n\n- Functions for retrieving available \n  [IAU](https://www.ta3.sk/IAUC22DB/MDC2007/Roje/roje_lista.php) registered meteor\n  showers.\n\n## Requirements\n\n- Python 3.7.1+, 3.8, 3.9 or 3.10\n\n## Installation\n\nYou can install `gmn-python-api` via [pip](https://pip.pypa.io/) from \n[PyPI](https://pypi.org/project/gmn-python-api/):\n\n```sh\npip install gmn-python-api\n```\n\nOr install the latest development code, through \n[TestPyPI](https://test.pypi.org/project/gmn-python-api/) or directly from \n[GitHub](https://github.com/rickybassom/gmn-python-api) via \n[pip](https://pip.pypa.io/):\n\n```sh\npip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gmn-python-api==<version>\n```\n\nOr\n\n```sh\npip install git+https://github.com/rickybassom/gmn-python-api\n```\n\nRefer to the [Troubleshooting] guide if you encounter any issues.\n\n## Usage\n\nSimple meteor analysis example:\n\n```python\nfrom gmn_python_api import data_directory as dd\nfrom gmn_python_api import meteor_trajectory_reader\n\n# Analyse recorded meteor data for the 24th of July 2019\ntraj_file_content = dd.get_daily_file_content_by_date("2019-07-24")\n\n# Read data as a Pandas DataFrame\ntraj_df = meteor_trajectory_reader.read_csv(traj_file_content)\n\nprint(f"{traj_df[\'Vgeo (km/s)\'].max()} km/s was the fastest geostationary velocity")\n# Output: 65.38499 km/s was the fastest geostationary velocity\n\nprint(f"{traj_df.loc[traj_df[\'IAU (code)\'] == \'PER\'].shape[0]} Perseid meteors")\n# Output: 8 Perseid meteors\n\nprint(\n  f"Station #{traj_df[\'Num (stat)\'].mode().values[0]} recorded the most meteors")\n# Output: Station #2 recorded the most meteors\n```\n\nPlease see the [Usage](https://gmn-python-api.readthedocs.io/en/latest/usage.html) and \n[API Reference](https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/index.html)\nsections for more details.\n\n## Contributing\nContributions are very welcome. To learn more, see the \n[Contributing guide].\n\n## License\n\nDistributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license,\n`gmn-python-api` is free and open source software.\n\n<!-- Links -->\n[Troubleshooting]: ./TROUBLESHOOTING.md\n[Contributing guide]: ./CONTRIBUTING.md\n',
    'author': 'Ricky Bassom',
    'author_email': 'rickybas12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rickybassom/gmn-python-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
