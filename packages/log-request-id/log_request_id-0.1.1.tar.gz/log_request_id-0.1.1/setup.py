# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log_request_id']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'log-request-id',
    'version': '0.1.1',
    'description': 'Log-Request-ID is extension for handling request-ID in logging.',
    'long_description': 'log-request-id\n=================\n\nLog-Request-ID is an extension to handle request-IDs logs in popular python api frameworks.\n\nCurrently supported frameworks: flask\n\nRequirements\n------------\n\n-  python (3.6+)\n\nInstalation\n-----------\n\nInstall using ``pip``\n\n::\n\n   pip install log-request-id\n\n\nUsage\n-----\n\n\n1. Set ``LOG_REQUEST_ID_FRAMEWORK_SUPPORT`` to point to your framework of choice (section currently supported).\n\n.. code:: txt\n\n    LOG_REQUEST_ID_FRAMEWORK_SUPPORT=flask\n\n2. Init request-ID handler\n\n-  Flask, with ``log_request_id.flask.init_flask_request_id_handler``\n\n.. code:: python\n\n   from log_request_id import init_flask_request_id_handler\n\n   def create_flask_app():\n       app = Flask()\n       init_flask_request_id_handler(app)\n\n3. Change log format (optional)\n\nAt this stage ``request_id`` is already present in log data, request-ID will be under ``request_id`` key.\n\n.. code:: python\n\n   logging.basicConfig(level=logging.WARNING, format=\'%(filename)s:%(levelname)s:%(request_id)s - %(message)s\')\n   # or\n   logging.getlogger().setformatter(logging.formatter("%(asctime)s:%(name)s:level=%(levelname)s:%(request_id)s - %(message)s"))\n\n\nFor more advanced logger configuration see `python\'s logging module <https://docs.python.org/3/library/logging.html>`_.\n\n``Warning`` if you will be adding custom handler or custom logging initialization use ``log_request_id.logging.RequestIdLogRecordFactory`` or ``log_request_id.logging.RequestIdLogFilter``.\n',
    'author': 'kuzxnia',
    'author_email': 'kacper.kuzniarski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
