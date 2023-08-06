# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['journai']

package_data = \
{'': ['*']}

install_requires = \
['folium>=0.14.0,<0.15.0',
 'jupyter>=1.0.0,<2.0.0',
 'ortools>=9.6.2534,<10.0.0',
 'pandas>=2.0.0,<3.0.0',
 'scikit-learn>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'journai-lib',
    'version': '0.1.0',
    'description': 'Let machine learning and operations research plan your next trip.',
    'long_description': '<h1 align="center">\n  <a href="#"><img src="./misc/journai.png" width="500"></a></br>\n  journai\n</h1>\n\n<p align="center">\n  Let <b>machine learning</b> and <b>operation research</b> plan your next trip.\n</p>\n\n---\n\n## ⚡️ Quick start\n\n```python\n>>> import pandas as pd\n>>> import journai as ji\n\n    # Get some data from the city you want to visit\n>>> df = pd.read_csv(\'bordeaux.csv\', sep=\';\')\n>>> df.head()\n    name                        kind    lat         lon\n0   Monument aux Girondins      place   44.84542    -0.57598\n1   Marche des Capucins         food    44.83087    -0.56762\n2   Grosse Cloche de Bordeaux   place   44.83577    -0.57143\n3   Pont Jacques Chaban Delmas  place   44.85866    -0.55204\n4   Tour Pey-Berland            place   44.83800    -0.57771\n\n    # Create a journai instance and display a map of your data\n>>> journai = ji.Journai()\n>>> journai.show_map(df)\n```\n\n<p align="center">\n  <a href="#"><img src="./docs/misc/map_bdx.png" width="550"></a>\n</p>\n\n```python\n    # use the clustering module to group different places\n>>> df[\'cluster\'] = journai.compute_cluster(df, nb_cluster=3)\n>>> journai.show_cluster(df)\n```\n\n<p align="center">\n  <a href="#"><img src="./docs/misc/cluster.png" width="550"></a>\n</p>\n\n```python\n    # run the tsp solver to get the right path between those places\n>>> df[\'tsp\'] = journai.compute_tsp(df)\n>>> journai.show_tsp(df)\n```\n\n<p align="center">\n  <a href="#"><img src="./docs/misc/tsp.png" width="550"></a>\n</p>\n\n## Philosophy\n\nPlanning trips is an exiting time for some... and a nightmare for others.\nPersonnaly, I rather prefer not to plan too much my travels. I just write a list of places I will be happy to visit and... that’s it. If I fail to go somewhere, that’s fine.\nHowever it happens that some travels are by far more chaotics than optimal...\nIt is in the economy of all effort that I built this tool over the years.\nAt first it was a wild Jupyter Notebook and it evolved into this current library.\n\nFor now, this lib has one job : to build a raw plan of your trip.\n\n### A [Vehicle Routing Problem](https://developers.google.com/optimization/routing/vrp#distance_matrix_api) ?\nIn my opinion, it can be if you have an hotel booked, viewed here as the "depot".\nBut this particular constraint is hard and I want my trip easy and flexible.\n\n### A [Traveling Salesman Problem](https://developers.google.com/optimization/routing/tsp) ?\nIt can be if you just have one day, but I would rather visit an area at a time so I would prefere to several separated planned loops.\n\n### A [Clustering Problem](https://scikit-learn.org/stable/modules/clustering.html) ?\nHere we go, clustering seems nice as it shows us adresses very close to each other, adding a tsp solver on each cluster and I think that we are good to go !\n\n### Visual map : [Folium](https://github.com/python-visualization/folium)\nWhat I really enjoyed during this project is its map display side.\nIt is a very eye pleasing thing to see clusters and tsp loops poping on the screen. It make the result quite tangible and even alive.\nAnd instead of having a ordered list of places to visit, you can build the html format version of the map, so you can acces it through your personal website or download it localy on your smartphone or computer and open it in your favorit browser.\n\nTo sum-up, `journai` stands on shoulder of geants like Google OR Tools, Scikit Learn and Folium, to make your planning stategy even easyer to create.\n\n## 🛠 Installation\n\n:snake: You need to install **Python 3.10** or above.\n\nInstallation can be done by using `pip`.\nThere are [wheels available](https://pypi.org/project/journai/#files) for **Linux**, **MacOS**, and **Windows**.\n\n```bash\npip install journai\n```\n\nYou can also install the latest development version as so:\n\n```bash\npip install git+https://github.com/tlentali/journai\n\n# Or, through SSH:\npip install git+ssh://git@github.com/tlentali/journai.git\n```\n\n## ⚙️ Under the hood\n\nYou can use this [site](https://www.gps-coordinates.net/) to convert an adress to lat-lon coordinates.\nThis project uses machine learning and operation research tools : a **great blend**.\n\nFirst, depending on the number of days you are staying, `journai` uses [Kmeans](https://scikit-learn.org/stable/modules/clustering.html#k-means) algorithm to regroup places into clusters.\nThen, a [Traveling Sellsman Problem](https://developers.google.com/optimization/routing/tsp) solver comes in hand to determine the shortest path to use between places in each cluster, starting from your staying place.\n\n## 🔥 Features\n\n- Generate clusters of places you want to see\n- Compute the TSP in each clusters\n- Show the map of our global trip displaying places you want to visit, by cluster and showing the TSP path\n- Data sample available for :\n  - London (UK)\n  - Paris (France)\n  - Copenhagen (Danemark)\n  - San Francisco (US)\n  - New York (US)\n  - Bristol (UK)\n  - Jaipur (India)\n  - Hanoi (Vietnam)\n  - Bordeaux (France)\n\n## 🖖 Contributing\n\nFeel free to contribute in any way you like, we\'re always open to new ideas and approaches. If you want to contribute to the code base please check out the [CONTRIBUTING.md](https://github.com/tlentali/journai/blob/master/CONTRIBUTING.md) file. Also take a look at the [issue tracker](https://github.com/tlentali/journai/issues) and see if anything takes your fancy.\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Again, contributions of any kind are welcome!\n\n## 📜 Licence\n\n`journai` is free and open-source software licensed under the [3-clause BSD license](https://github.com/tlentali/journai/blob/master/LICENSE).\n',
    'author': 'tlentali',
    'author_email': 'thomas.lentali@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
