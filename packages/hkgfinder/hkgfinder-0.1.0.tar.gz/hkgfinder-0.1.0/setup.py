# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hkgfinder']

package_data = \
{'': ['*']}

install_requires = \
['bio>=1.3.9,<2.0.0', 'pyfastx>=0.8.4,<0.9.0', 'xphyle>=4.4.2,<5.0.0']

entry_points = \
{'console_scripts': ['hkgfinder = hkgfinder.hkgfinder:main']}

setup_kwargs = {
    'name': 'hkgfinder',
    'version': '0.1.0',
    'description': 'find housekeeping genes in prokaryotic (meta)genomic data',
    'long_description': "# hkgfinder\n\n[![PyPI](https://img.shields.io/pypi/v/hkgfinder.svg)](https://pypi.org/project/hkgfinder)\n[![Wheel](https://img.shields.io/pypi/wheel/hkgfinder.svg)](https://pypi.org/project/hkgfinder)\n[![Language](https://img.shields.io/pypi/implementation/hkgfinder)](https://pypi.org/project/hkgfinder)\n[![Pyver](https://img.shields.io/pypi/pyversions/hkgfinder.svg)](https://pypi.org/project/hkgfinder)\n[![Downloads](https://img.shields.io/pypi/dm/hkgfinder)](https://pypi.org/project/hkgfinder)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://www.gnu.org/licenses/MIT)\n\n\n## Find housekeeping genes in prokaryotic (meta)genomes\n\n### Introduction\nhkgfinder is a fast and accurate housekeeping gene finder and classifier. Hkgfinder can run on raw sequences, genomes and metagenomes. The novel value of this method lies is in its ability to directly predict and classify gene sequences into housekeeping gene families at a high specificity and sensitivity, while being also faster than genome and metagenome annotator on genome and metagenome data.\n\n### How hkgfinder works\n![](img/hkgfinder.png)\n\n### Installation\n\nYou will have first to install [Prodigal](https://github.com/hyattpd/Prodigal) and [HMMER 3](https://hmmer.org) to be able to run hkgfinder.\n\n\n#### Install from Pip\n\n```bash\npip install hkgfinder\n```\n\n\n#### Install from source\n\n```bash\n# Download hkgfinder development version\ngit clone https://github.com/Ebedthan/hkgfinder.git hkgfinder\n\n# Navigate to directory\ncd hkgfinder\n\n# Install with poetry: see https://python-poetry.org\npoetry install --no-dev\n\n# Enter the Python virtual environment with\npoetry shell\n\n# Test hkgfinder is correctly installed\nhkgfinder -h\n```\n\nIf you do not want to go into the virtual environment just do:\n\n```bash\npoetry run hkgfinder -h\n```\n\n## Test\n\n* Type `hkgfinder -h` and it should output something like:\n\n```\nusage: hkgfinder [options] [<FILE>]\n\noptional arguments:\n  -o [FILE]      output result to FILE [stdout]\n  -g             activate genome mode [false]\n  -m             activate metagenome mode [false]\n  --faa FILE     output matched proteins sequences to FILE\n  --fna FILE     output matched DNA sequences to FILE\n  -t INT         number of threads [1]\n  -q             decrease program verbosity\n  -v, --version  show program's version number and exit\n  -h, --help     show this help message and exit\n```\n\n\n## Invoking hkgfinder\n\n```\nhkgfinder --faa housekeeping.faa --fna housekeeping.fna file.fa.gz\n```\n\n* hkgfinder supports gzip, lzma, bz2 and zstd compressed files.\n  \n## Bugs\n\nSubmit problems or requests to the [Issue Tracker](https://github.com/Ebedthan/hkgfinder/issues).\n\n\n## Dependencies\n\n### Mandatory\n\n* [**Prodigal**](https://github.com/sib-swiss/pftools3)  \n  Used for protein-coding gene prediction.    \n  *Hyatt, D., Chen, GL., LoCascio, P.F. et al. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics 11, 119 (2010). https://doi.org/10.1186/1471-2105-11-119*\n\n* [**HMMER 3**](https://hmmer.org)  \n  Used for HMM profile prediction.   \n  *Eddy SR, Accelerated Profile HMM Searches. PLOS Computational Biology 2011, 10.1371/journal.pcbi.1002195*\n\n\n## Licence\n\n[MIT](https://github.com/Ebedthan/hkgfinder/blob/main/LICENSE).\n\n\n## Author\n\n* [Anicet Ebou](https://orcid.org/0000-0003-4005-177X)\n\n",
    'author': 'Anicet Ebou',
    'author_email': 'anicet.ebou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ebedthan/hkgfinder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
