# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libera_utils', 'libera_utils.backports', 'libera_utils.db', 'libera_utils.io']

package_data = \
{'': ['*'],
 'libera_utils': ['data/config.json',
                  'data/config.json',
                  'data/jpss1_geolocation_xtce_v1.xml',
                  'data/jpss1_geolocation_xtce_v1.xml',
                  'data/spice/*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0',
 'astropy>=5.1,<6.0',
 'cloudpathlib[s3]>=0,<1',
 'h5netcdf>=1.1.0,<2.0.0',
 'h5py>=3.3,<4.0',
 'lasp-packets>=2.0,<3.0',
 'numpy>=1.21,<2.0',
 'psycopg2>=2.9,<3.0',
 'requests>=2.26,<3.0',
 'setuptools>=65',
 'spiceypy>=5.0,<6.0',
 'watchtower>=3.0,<4.0',
 'xarray>=2023.1.0,<2024.0.0']

entry_points = \
{'console_scripts': ['libera-utils = libera_utils.cli:main']}

setup_kwargs = {
    'name': 'libera-utils',
    'version': '2.1.0',
    'description': 'Utility package for Libera Science Data Processing and the Libera Science Data Center. Copyright 2022 University of Colorado.',
    'long_description': 'None',
    'author': 'Stephane Beland',
    'author_email': 'stephane.beland@lasp.colorado.edu',
    'maintainer': 'Gavin Medley',
    'maintainer_email': 'gavin.medley@lasp.colorado.edu',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
