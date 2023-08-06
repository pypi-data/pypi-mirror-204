# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_fastapi_pw']

package_data = \
{'': ['*']}

install_requires = \
['about-time>=4.2.1,<5.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'logzero>=1.6.3,<2.0.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'playwright>=1.32.1,<2.0.0',
 'portalocker>=2.7.0,<3.0.0',
 'pyquery>=2.0.0,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['deepl-fastapi-pw = deepl_fastapi_pw.run_uvicorn:main']}

setup_kwargs = {
    'name': 'deepl-fastapi-pw',
    'version': '0.1.0a1',
    'description': 'deepl via fastapi using deepl-scraper-pw',
    'long_description': '# deepl-fastapi-pw\n<!--- repo-name  pypi-name  mod_name func_name --->\n[![tests](https://github.com/ffreemt/deepl-fastapi-playwright/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-fastapi.svg)](https://badge.fury.io/py/deepl-fastapi-pw)\n\nYour own deepl server via fastapi and playwright, cross-platform (Windows/Linux/MacOs) with API for OmegaT\n\n## Installation\n*   Create a virual environment: optional but recommended\n    e.g.,\n    ```bash\n    # Linux and friends\n    python3.7 -m venv .venv\n    source .venv/bin/activate\n\n    # Windows\n    # py -3.7 -m venv .venv\n    # .venv\\Scripts\\activate\n    ```\n\n```bash\npip install deepl-fastapi-pw\n```\nor (if your use poetry)\n```bash\npoetry add deepl-fastapi-pw\n```\nor\n```\n pip install git+https://github.com/ffreemt/deepl-fastapi-playwright.git\n```\nor\n*   Clone the repo [https://github.com/ffreemt/deepl-fastapi-playwright.git](https://github.com/ffreemt/deepl-fastapi-playwrigh.git)\n    ```bash\n    git clone https://github.com/ffreemt/deepl-fastapi-playwright.git\n    ```\n    and `cd deepl-fastapi-playwright`\n*   `pip install -r requirements.txt\n    * or ``poetry install``\n\n## Usage\n\n*   Start the server\n\nUse uvicorn directly (note the `deepl_server` module, not `run_uvicorn`)\n```bash\nuvicorn deepl_fastapi_pw.deepl_server_async:app\n```\n\nor\n```bash\npython  -m deepl_fastapi_pw.deepl_server_async\n```\n\nor run the server on the external net, for example at port 9888\n```\nuvicorn deepl_fastapi_pw.deepl_server:app --reload --host 0.0.0.0 --port 9888\n```\n\n*   Explore and consume\n\nPoint your browser to [http://127.0.0.1:8001/text/?q=test&to_lang=zh](http://127.0.0.1:8000/text/?q=test&to_lang=zh)\n\nOr in python code (`pip install requests` first)\n```python\nimport requests\n\n# get\nurl =  "http://127.0.0.1:8001/text/?q=test me&to_lang=zh"\nprint(requests.get(url).json())\n# {\'q\': \'test me\', \'from_lang\': None, \'to_lang\': \'zh\',\n# \'trtext\': \'考我 试探我 测试我 试探\'}\n\n# post\ntext = "test this and that"\ndata = {"text": text, "to_lang": "zh"}\nresp = requests.post("http://127.0.0.1:8001/text", json=data)\nprint(resp.json())\n# {\'q\': {\'text\': \'test this and that\', \'from_lang\': None, \'to_lang\': \'zh\', \'description\': None},\n# \'result\': \'试探 左右逢源 检验 审时度势\'}\n\n```\n\n## Interactive Docs (Swagger UI)\n\n [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)\n',
    'author': 'freemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/deepl-fastapi-playwright',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
