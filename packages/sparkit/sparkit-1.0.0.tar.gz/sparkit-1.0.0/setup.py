# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sparkit']

package_data = \
{'': ['*']}

install_requires = \
['bumbag>=4.0.1,<5.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyarrow>=11.0.0,<12.0.0',
 'pyspark>=3,<4']

setup_kwargs = {
    'name': 'sparkit',
    'version': '1.0.0',
    'description': 'A package for PySpark utility functions.',
    'long_description': '<p align="center">\n<img src="https://raw.githubusercontent.com/estripling/sparkit/main/docs/source/_static/logo.png" width="480" alt="The sparkit logo.">\n</p>\n\n<p align="center">\n<a href="https://pypi.org/project/sparkit"><img alt="pypi" src="https://img.shields.io/pypi/v/sparkit"></a>\n<a href="https://readthedocs.org/projects/sparkit/?badge=latest"><img alt="docs" src="https://readthedocs.org/projects/sparkit/badge/?version=latest"></a>\n<a href="https://github.com/estripling/sparkit/actions/workflows/ci.yml"><img alt="ci status" src="https://github.com/estripling/sparkit/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n<a href="https://codecov.io/gh/estripling/sparkit"><img alt="coverage" src="https://codecov.io/github/estripling/sparkit/coverage.svg?branch=main"></a>\n<a href="https://github.com/estripling/sparkit/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/pypi/l/sparkit"></a>\n</p>\n\n## About\n\nA package for PySpark utility functions:\n\n- [Documentation](https://sparkit.readthedocs.io/en/stable/index.html)\n- [Example usage](https://sparkit.readthedocs.io/en/stable/example.html)\n- [API Reference](https://sparkit.readthedocs.io/en/stable/autoapi/sparkit/index.html)\n\n## Installation\n\n`sparkit` is available on [PyPI](https://pypi.org/project/sparkit/) for Python 3.8+ and Spark 3 (Java 11):\n\n```console\npip install sparkit\n```\n\n## Examples\n\n[`join`](https://sparkit.readthedocs.io/en/stable/autoapi/sparkit/index.html#sparkit.join) multiple data frames on common key (pass single and / or an iterable of data frames):\n\n```python\n>>> import sparkit\n>>> from pyspark.sql import Row, SparkSession\n>>> spark = SparkSession.builder.getOrCreate()\n>>> df1 = spark.createDataFrame([Row(id=1, x="a"), Row(id=2, x="b")])\n>>> df2 = spark.createDataFrame([Row(id=1, y="c"), Row(id=2, y="d")])\n>>> df3 = spark.createDataFrame([Row(id=1, z="e"), Row(id=2, z="f")])\n>>> sparkit.join([df1, df2], df3, on="id").show()\n+---+---+---+---+\n| id|  x|  y|  z|\n+---+---+---+---+\n|  1|  a|  c|  e|\n|  2|  b|  d|  f|\n+---+---+---+---+\n```\n\n[`union`](https://sparkit.readthedocs.io/en/stable/autoapi/sparkit/index.html#sparkit.union) multiple data frames by name (pass single and / or an iterable of data frames):\n\n```python\n>>> import sparkit\n>>> from pyspark.sql import Row, SparkSession\n>>> spark = SparkSession.builder.getOrCreate()\n>>> df1 = spark.createDataFrame([Row(x=1, y=2), Row(x=3, y=4)])\n>>> df2 = spark.createDataFrame([Row(x=5, y=6), Row(x=7, y=8)])\n>>> df3 = spark.createDataFrame([Row(x=0, y=1), Row(x=2, y=3)])\n>>> df4 = spark.createDataFrame([Row(x=5, y=3), Row(x=9, y=6)])\n>>> sparkit.union(df1, [df2, df3], df4).show()\n+---+---+\n|  x|  y|\n+---+---+\n|  1|  2|\n|  3|  4|\n|  5|  6|\n|  7|  8|\n|  0|  1|\n|  2|  3|\n|  5|  3|\n|  9|  6|\n+---+---+\n```\n\n## Contributing to sparkit\n\nYour contribution is greatly appreciated!\nSee the following links to help you get started:\n\n- [Contributing Guide](https://sparkit.readthedocs.io/en/latest/contributing.html)\n- [Developer Guide](https://sparkit.readthedocs.io/en/latest/developers.html)\n- [Contributor Code of Conduct](https://sparkit.readthedocs.io/en/latest/conduct.html)\n\n## License\n\n`sparkit` was created by sparkit Developers.\nIt is licensed under the terms of the BSD 3-Clause license.\n',
    'author': 'sparkit Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/estripling/sparkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
