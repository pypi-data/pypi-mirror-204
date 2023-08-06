# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libsql_client', 'libsql_client.hrana']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0,<4.0']

setup_kwargs = {
    'name': 'libsql-client',
    'version': '0.2.0',
    'description': 'Python SDK for libSQL',
    'long_description': '# Python SDK for libSQL\n\n**[API reference][reference] | [Github][github] | [PyPI][pypi]**\n\n[reference]: https://libsql.org/libsql-client-py/reference.html\n[github]: https://github.com/libsql/libsql-client-py\n[pypi]: https://pypi.org/project/libsql-client/\n\nThis is the source repository of the Python SDK for libSQL. You can either connect to a local SQLite database or to a remote libSQL server ([sqld][sqld]).\n\n[sqld]: https://github.com/libsql/sqld\n\n## Installation\n\n```\npip install libsql-client\n```\n\n## Getting Started\n\nConnecting to a local SQLite database:\n\n```python\nimport asyncio\nimport libsql_client\n\nasync def main():\n    url = "file:local.db"\n    async with libsql_client.create_client(url) as client:\n        result_set = await client.execute("SELECT * from users")\n        print(len(result_set.rows), "rows")\n        for row in result_set.rows:\n            print(row)\n\nasyncio.run(main())\n```\n\nTo connect to a remote libSQL server ([sqld][sqld]), just change the URL:\n\n```python\nurl = "ws://localhost:8080"\n```\n\n## Supported URLs\n\nThe client can connect to the database using different methods depending on the scheme (protocol) of the passed URL:\n\n* `file:` connects to a local SQLite database (using the builtin `sqlite3` package)\n  * `file:/absolute/path` or `file:///absolute/path` is an absolute path on local filesystem\n  * `file:relative/path` is a relative path on local filesystem\n  * (`file://path` is not a valid URL)\n* `ws:` or `wss:` connect to sqld using WebSockets (the Hrana protocol).\n* `http:` or `https:` connect to sqld using HTTP. The `transaction()` API is not available in this case.\n* `libsql:` is equivalent to `wss:`.\n\n## Synchronous API\n\nThis package also provides a synchronous version of the client, which can be created by calling `create_client_sync()`. It supports the same methods as the default `asyncio` client, except that they block the calling thread:\n\n```python\nimport libsql_client\n\nurl = "file:local.db"\nwith libsql_client.create_client(url) as client:\n    result_set = client.execute("SELECT * from users")\n    print(len(result_set.rows), "rows")\n    for row in result_set.rows:\n        print(row)\n```\n\nThe synchronous client is just a thin wrapper around the asynchronous client, but it runs the event loop in a background thread.\n\n## Contributing to this package\n\nFirst, please install Python and [Poetry][poetry]. To install all dependencies for local development to a\nvirtual environment, run:\n\n[poetry]: https://python-poetry.org/\n\n```\npoetry install --with dev\n```\n\nTo run the tests, use:\n\n```\npoetry run pytest\n```\n\nTo check types with MyPy, use:\n\n```\npoetry run mypy\n```\n\n## License\n\nThis project is licensed under the MIT license.\n\n### Contribution\n\nUnless you explicitly state otherwise, any contribution intentionally submitted for inclusion in `libsql-client` by you, shall be licensed as MIT, without any additional terms or conditions.\n',
    'author': 'Jan Špaček',
    'author_email': 'honza@chiselstrike.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/libsql/libsql-client-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
