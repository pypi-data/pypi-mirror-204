# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiofauna']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiohttp-sse>=2.1.0,<3.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'aiohttp_cors>=0.7.0,<0.8.0',
 'iso8601>=1.1.0,<2.0.0',
 'pydantic[dotenv,email]>=1.10.7,<2.0.0']

entry_points = \
{'console_scripts': ['aiofauna = aiofauna.cli:cli']}

setup_kwargs = {
    'name': 'aiofauna',
    'version': '0.0.32',
    'description': 'FaunaDB + Aiohttp fullstack framework',
    'long_description': '---\ntitle: AioFauna\n---\n\n# AioFauna\n\n🚀 Introducing aiofauna: A powerful library to supercharge your FaunaDB experience with modern async Python frameworks! 🔥\n\n🌟 Features:\n\n✅ Async/await coroutines: Leverage the power of async programming for enhanced\nperformance and responsiveness.\n\n✅ SSE (Server-Sent Events) support: Stream data in real-time to your clients.\n\n✅ Pydantic-based Document Object Mapper (DOM): Define and validate your data models with ease.\n\n✅ Auto-provisioning: Automatic management of indexes, unique indexes, and collections.\n\n✅ Standardized CRUD operations: Simplify your interactions with FaunaDB using find, find_unique, find_many, find_all, create, upsert, delete, and query methods.\n\n✅ Full JSON communication: Custom encoders to ensure seamless data exchange between your application and FaunaDB backend.\n\n✅ ASGI compliant: `aiofauna.asgi` module provides a middleware to convert `aiohttp.web.Application` into an ASGI application.\n\n💡 With aiofauna, you can build fast, scalable, and reliable applications using the power of FaunaDB and modern asynchronous Python with its out of the box `aiohttp` based web framework. Say goodbye to the hassle of manually managing indexes and collections and hello to a seamless data driven development experience with Pydantic.\n\n🌐 aiofauna is independent and allows native interaction with external services like Docker API, GCP API, AWS API among others, implementing a lightweight stack with aiohttp server capabilities and fauna backend (to be enhanced soon).\n\n📚 Check out the aiofauna library, and start building your next-gen applications today! 🚀\n#Python #FaunaDB #Async #Pydantic #aiofauna\n\n⚙️ If you are using a synchronous framework check out [Faudantic](https://github.com/obahamonde/faudantic) for a similar experience with FaunaDB and Pydantic.\n\n📚 [Documentation](https://aiofauna.smartpro.solutions)\n\n📦 [PyPi](https://pypi.org/project/aiofauna/)\n\n📦 [GitHub](https://github.com/obahamonde/aiofauna)\n\n📦 [Demo](https://aiofaunastreams-fwuw7gz7oq-uc.a.run.app/) (Stream data in real-time to your clients)\n',
    'author': 'Oscar Bahamonde',
    'author_email': 'oscar.bahamonde.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/obahamonde/aiofauna',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
