# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nunchaku']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.4,<2.0',
 'scipy>=1.7.3,<2.0.0',
 'sympy>=1.9,<2.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'nunchaku',
    'version': '0.10.0',
    'description': 'Dividing data into linear segments.',
    'long_description': '# nunchaku: Dividing data into linear segments\n\n`nunchaku` is a Python module for dividing data into linear segments.\nIt answers two questions:\n1. how many linear segments best fit the data without overfitting (by Bayesian model comparison);\n2. given the number of linear segments, where the boundaries between them are (by finding the posterior of the boundaries).\n\n## Installation\nFor users, type in terminal\n```\n> pip install nunchaku\n```\n\nFor developers, create a virtual environment and then install with Poetry: \n```\n> git clone https://git.ecdf.ed.ac.uk/s1856140/nunchaku.git\n> cd nunchaku \n> poetry install --with dev \n```\n\n## Quickstart\nData `x` is a list or a 1D Numpy array, sorted ascendingly; the data `y` is a list or a Numpy array, with each row being one replicate of measurement.\n```\n>>> from nunchaku.nunchaku import nunchaku, get_example_data\n>>> x, y = get_example_data()\n>>> nc = nunchaku(x, y, prior=[-5,5]) # load data and set prior of gradient\n>>> # compare models with 1, 2, 3 and 4 linear segments\n>>> numseg, evidences = nc.get_number(max_num=4)\n>>> # get the mean and standard deviation of the boundary points\n>>> bds, bds_std = nc.get_iboundaries(numseg)\n>>> # get the information of all segments\n>>> info_df = nc.get_info(bds)\n>>> # plot the data and the segments\n>>> nc.plot(info_df)\n```\n\n## Documentation\nDetailed documentation is available on [Readthedocs](https://nunchaku.readthedocs.io/en/latest/).\n\n## Citation\nA preprint is coming soon.\n',
    'author': 'Yu Huo',
    'author_email': 'yu.huo@ed.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://nunchaku.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
