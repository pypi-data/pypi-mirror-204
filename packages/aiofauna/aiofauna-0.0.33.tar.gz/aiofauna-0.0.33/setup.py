# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiofauna']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiohttp-devtools',
 'aiohttp-sse>=2.1.0,<3.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'aiohttp_cors>=0.7.0,<0.8.0',
 'iso8601>=1.1.0,<2.0.0',
 'pydantic[dotenv,email]>=1.10.7,<2.0.0']

entry_points = \
{'console_scripts': ['aiofauna = aiofauna.cli:cli']}

setup_kwargs = {
    'name': 'aiofauna',
    'version': '0.0.33',
    'description': 'Fullstack DX/API First Cloud centric framework',
    'long_description': '---\ntitle: AioFauna\n---\n\n# AioFauna\n \n 🚀 Introducing aiofauna: A full-stack framework for FaunaDB, industry performant with a seamless user experience! 🔥 Take your Backend Development to the next level dramatically improving productivity, performance and development experience.\n\n🌟 Features:\n\n✅ Inspired by FastAPI: DX (Developer Experience) first. Based on Pydantic, Aiohttp, and FaunaDB. CORS support, query and path parameters, request body parsing, most of the features you love from FastAPI are available in aiofauna.\n\n✅ Blazingly Fast!: Industry performant http server while having the fastest python based http client allowing exceptional integrations with third party APIs, forget about installing dozens of SDKs.\n\n✅ Async/await coroutines: Leverage the power of async programming for enhanced performance and responsiveness. \n\n✅ Automatic Swagger UI generation: Automatic documentation and manual testing UI following industry standard without further effort!.\n\n✅ Live reload and SSE (Server-Sent Events) support: Stream data in real-time to your clients and experience effortless development with live reload.\n\n✅ Pydantic-based Document Object Mapper (DOM): Define and validate your data models with ease. Summarize complex FQL expressions into pythonic, fully typed asynchronous methods for all CRUD operations.\n\n✅ Auto-provisioning: Automatic management of indexes, unique indexes, and collections.\n\n✅ Full JSON communication: Custom encoders to ensure seamless data exchange between your application and FaunaDB backend.\n\n✅ ASGI compliant: provides an ASGI adapter, allowing broader integration with _asgi_ servers like `uvicorn`, `tornado` or `daphne`.\n\n💡 With aiofauna, you can build fast, scalable, and reliable applications using the power of FaunaDB and modern asynchronous Python with its out of the box aiohttp based web framework. Say goodbye to the hassle of manually managing indexes and collections and hello to a seamless data driven development experience with FaunaModel.\n\n🌐 aiofauna is independent and allows native interaction with external services like Docker API, GCP API, AWS API among others, implementing a lightweight stack with aiohttp server capabilities and fauna backend (to be enhanced soon).\n\n📚 Check out the aiofauna library, and start building your next-gen applications today! 🚀\n#Python #FaunaDB #Async #Pydantic #aiofauna\n\n⚙️ If you are using a synchronous framework check out [Faudantic](https://github.com/obahamonde/faudantic) for a similar experience with FaunaDB and Pydantic.\n\n📚 [Documentation](https://aiofauna.smartpro.solutions)\n\n📦 [PyPi](https://pypi.org/project/aiofauna/)\n\n📦 [GitHub](https://github.com/obahamonde/aiofauna)\n\n📦 [Demo](https://aiofaunastreams-fwuw7gz7oq-uc.a.run.app/) (Stream data in real-time to your clients)\n',
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
