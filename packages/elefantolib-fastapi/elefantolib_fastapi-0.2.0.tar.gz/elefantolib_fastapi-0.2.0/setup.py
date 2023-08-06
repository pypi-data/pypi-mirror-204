# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elefantolib_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['elefantolib>=0.9.2,<0.10.0', 'fastapi>=0.95.1,<0.96.0']

setup_kwargs = {
    'name': 'elefantolib-fastapi',
    'version': '0.2.0',
    'description': '',
    'long_description': '## Elefantolib for FastAPI\n\n> **_NOTE:_**  Only for this library developers. After clone this repository you should run command:\n> \n\n ```console \ngit config core.hooksPath .githooks\n```\n\n\n## Installation\n\n<div class="termy">\n\n```console\npoetry add elefantolib-fastapi\n```\n</div>\n\n## Example\n\n### Prepare\n\n* Add environmental variables\n\n```\nSECRET=\nALGORITHM=\nISSUER=\n```\n* Defaults:\n    \n    - SECRET - not set, this is required\n    - ALGORITHM=HS256\n    - ISSUER=Consumer\n\n### Create it\n\n* Create a file `main.py` with:\n\n```Python\nfrom elefantolib_fastapi.requests import ElefantoRequest\nfrom elefantolib_fastapi.routes import ElefantoRoute\n\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\napp.router.route_class = ElefantoRoute\n\n\n@app.get(\'/\')\ndef index(request: ElefantoRequest):\n    # TODO something\n    response = request.pfm.services.some_service_name.get(\'path-to-endpoint\')\n    return response\n\n```',
    'author': 'gglassota',
    'author_email': 'gglassota2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
