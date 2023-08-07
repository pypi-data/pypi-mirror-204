# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owid', 'owid.repack']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.0,<2.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'owid-repack',
    'version': '0.1.2',
    'description': 'Pack Pandas data frames into smaller, more memory-efficient data types.',
    'long_description': '# owid-repack-py\n\n![build status](https://github.com/owid/owid-repack-py/actions/workflows/python-package.yml/badge.svg)\n[![PyPI version](https://badge.fury.io/py/owid-repack.svg)](https://badge.fury.io/py/owid-repack)\n![](https://img.shields.io/badge/python-3.8|3.9|3.10|3.11-blue.svg)\n\n_Pack Pandas DataFrames into smaller, more memory efficient types._\n\n## Overview\n\nWhen you load data into Pandas, it will use standard types by default:\n\n- `object` for strings\n- `int64` for integers\n- `float64` for floating point numbers\n\nHowever, for many datasets there is a much more compact representation that Pandas could be using for that data. Using a more compact representation leads to lower memory usage, and smaller binary files on disk when using formats such as Feather and Parquet.\n\nThis library does just one thing: it shrinks your data frames to use smaller types.\n\n## Installing\n\n`pip install owid-repack`\n\n## Usage\n\nThe `owid.repack` module exposes two methods, `repack_series()` and `repack_frame()`.\n\n`repack_series()` will detect the smallest type that can accurately fit the existing data in the series.\n\n```ipython\nIn [1]: from owid import repack\n\nIn [2]: pd.Series([1, 2, 3])\nOut[2]:\n0    1\n1    2\n2    3\ndtype: int64\n\nIn [3]: repack.repack_series(pd.Series([1.5, 2, 3]))\nOut[3]:\n0    1.5\n1    2.0\n2    3.0\ndtype: float32\n\nIn [4]: repack.repack_series(pd.Series([1, None, 3]))\nOut[4]:\n0       1\n1    <NA>\n2       3\ndtype: UInt8\n\nIn [5]: repack.repack_series(pd.Series([-1, None, 3]))\nOut[5]:\n0      -1\n1    <NA>\n2       3\ndtype: Int8\n```\n\nThe `repack_frame()` method simply does this across every column in your DataFrame, returning a new DataFrame.\n\n## Releases\n\n- `0.1.2`:\n    - Shrink columns with all NaNs to Int8\n- `0.1.1`:\n    - Fix Python support in package metadata to support 3.8.1 onwards\n- `0.1.0`:\n  - Migrate first version from `owid-catalog-py` repo\n',
    'author': 'Our World In Data',
    'author_email': 'tech@ourworldindata.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/owid/owid-catalog-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
