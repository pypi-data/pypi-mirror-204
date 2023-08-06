# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyaemet', 'pyaemet.static', 'pyaemet.types_classes', 'pyaemet.utilities']

package_data = \
{'': ['*'], 'pyaemet.static': ['sites/*']}

install_requires = \
['folium>=0.14.0,<0.15.0',
 'geocoder>=1.38.1,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.3,<2.0.0',
 'pandas>=2.0.1,<3.0.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'pyaemet',
    'version': '1.0.5rc1',
    'description': 'Python module to interact with the AEMET API to download meteorological data',
    'long_description': '# pyAEMET\n\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyaemet.svg)](https://pypi.org/project/pyaemet/)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5655307.svg)](https://doi.org/10.5281/zenodo.5655307)\n[![License](https://img.shields.io/pypi/l/pandas.svg)](https://github.com/jaimedgp/pyAEMET/blob/main/LICENSE)\n[![Downloads](https://static.pepy.tech/personalized-badge/pyaemet?period=month&units=international_system&left_color=gray&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/pyaemet)\n\nA python library developed to download daily climatological values from the Spanish National\nMeteorological Agency (AEMET) through its OpenData API. The library contains several methods\nto facilitate downloading and filtering the climatological data.\n\n> The information that this library collects and uses is property of the Spanish State\n> Meteorological Agency, available through its AEMET OpenData REST API.\n\n\n## Installation\n``` bash\n$ pip install pyaemet\n```\nTo use the pyAEMET module, you need to get an API key from the AEMET (Spanish State Meteorological\nAgency) OpenData platform. You can apply for a key [here](https://opendata.aemet.es/centrodedescargas/altaUsuario).\n\n## Usage\n\nOnce the module is installed and you have your API key, you can start using the module by\nimporting it in your Python script. To use the module\'s functions, you need to initialize\nthe client with your API key:\n\n```python\nimport pyaemet\n\naemet = pyaemet.AemetClima(api_key)\n```\n\nThe `AemetClima` class takes an API key as a parameter in its constructor and allows you to get\ninformation about the available monitoring sites, filter sites based on different parameters\n(e.g., city, province, autonomous community), and get nearby sites to a specific location.\n\nHere is a summary of some of the methods provided by the `AemetClima` class:\n\n* **`sites_info`**: Retrieves information about all the available monitoring sites. The method\nreturns an instance of the `SitesDataFrame` class, which is a subclass of the pandas `DataFrame`.\n```python\naemet.sites_info(update=True)\n```\n\n* **`sites_in`**: Filters the available monitoring sites based on specified parameters\n(e.g., city, province, autonomous community). The method returns an instance of the `SitesDataFrame` class.\n```python\naemet.sites_in(subregion="Cantabria")\n```\n![image](https://github.com/Jaimedgp/pyAEMET/raw/main/docs/screenshots/sites_cantabria.png)\n\n* **`near_sites`**: Retrieves the ``n_near`` monitoring sites closest to a specified latitude and longitude,\nwithin a maximum distance of `max_distance` kilometers. The method returns an instance of the\n`NearSitesDataFrame` class.\n```python\naemet.near_sites(latitude=43.47,\n                 longitude=-3.798,\n                 n_near=5, max_distance=50)\n```\n![image](https://github.com/Jaimedgp/pyAEMET/raw/main/docs/screenshots/near_sites.png)\n\n* **`sites_curation`**: Retrieves the amount of available data of certain `variables` in the monitoring `sites` in a period of time defined by\n    `start_dt` and `end_dt`. The function returns a `SitesDataFrame` or `NearSitesDataFrame` (depends of the type of the `sites` parameter given)\n    with a column with the average `amount` between all `variables` and `has_enough` boolean if the amount is greater or equal to a `threshold`.\n\n* **`daily_clima`**: Retrieves daily climate data for a given ``site`` or a list of sites over a\nspecified date range defined by `start_dt` and `end_dt`. The function returns a\n`ObservationsDataFrame` object, which is a data structure that holds the retrieved climate data\nalong with any associated metadata.\n```python\nimport datetime\naemet.daily_clima(site=aemet.sites_in(city="Santander"),\n                  start_dt=datetime.date(2022, 6, 3),\n                  end_dt=datetime.date.today())\n```\n\nThe module also provides three deprecated methods `estaciones_info`, `estaciones_loc` and `clima_diaria`\nthat perform similar functionality as the `sites_info`, `sites_in` and `daily_clima` methods, respectively.\n\nYou can find the complete documentation of the module\'s functions in the GitHub repository,\nunder the docs directory.\n\n## FAQ\n## Contributing\n## References\n* ["Estimating changes in air pollutant levels due to COVID-19 lockdown measures based on a business-as-usual prediction scenario using data mining models: A case-study for urban traffic sites in Spain"](https://doi.org/10.1016/j.scitotenv.2022.153786), submitted to Environmental Software & Modelling by [J. González-Pardo](https://orcid.org/0000-0001-7268-9933) et al. (2021)\n',
    'author': 'Jaimedgp',
    'author_email': 'jaime.diez.gp@gmail.com',
    'maintainer': 'CarmenGBM',
    'maintainer_email': 'carmen.garcia.be96@gmail.com',
    'url': 'https://github.com/jaimedgp/pyAEMET',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
