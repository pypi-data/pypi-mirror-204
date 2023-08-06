# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['league_client_live_data', 'league_client_live_data.endpoint_data']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.3.0,<24.0.0',
 'httpx>=0.24.0,<0.25.0',
 'mypy>=1.2.0,<2.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'pylint>=2.17.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'ruff>=0.0.262,<0.0.263',
 'types-pyyaml>=6.0.12.9,<7.0.0.0']

setup_kwargs = {
    'name': 'leagueclientlivedata',
    'version': '0.1.0',
    'description': '',
    'long_description': '# League Client Live Data Api\nAn async api wrapper for the [game client api](https://developer.riotgames.com/docs/lol#game-client-api) from league of legends.\nFor every endpoint there is a pydantic BaseModel that represents the data from the response of the request. \n# Setup\n## Installation\n\n```bash\ngit clone https://github.com/Plutokekz/LeagueClientLiveDataApi.git\npoetry install\n```\n## Usage\nGet the events from your current game\n````python\nfrom pathlib import Path\n\nfrom live_client_data import LeagueClientLiveDataApi\n\n\nif __name__ == "__main__":\n    config_file = Path("config.yaml")\n    api = LeagueClientLiveDataApi()\n    async def main():\n        while True:\n            data = await api.event_data()\n            print(data)\n    api.loop.run_until_complete(main())\n````\n## Config\n\nthe config file contains currently 2 entries on for the api endpoint and one for the \nssl certificate of riot games. You can download the file from [here](https://developer.riotgames.com/docs/lol#game-client-api). \n\n````yaml\ncert_file: "riotgames.pem"\nurl: "https://127.0.0.1:2999/liveclientdata"\n````\n',
    'author': 'Lukas Mahr',
    'author_email': 'lukas@yousuckatprogramming.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
