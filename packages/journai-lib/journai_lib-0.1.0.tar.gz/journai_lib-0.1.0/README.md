<h1 align="center">
  <a href="#"><img src="./misc/journai.png" width="500"></a></br>
  journai
</h1>

<p align="center">
  Let <b>machine learning</b> and <b>operation research</b> plan your next trip.
</p>

---

## ⚡️ Quick start

```python
>>> import pandas as pd
>>> import journai as ji

    # Get some data from the city you want to visit
>>> df = pd.read_csv('bordeaux.csv', sep=';')
>>> df.head()
    name                        kind    lat         lon
0   Monument aux Girondins      place   44.84542    -0.57598
1   Marche des Capucins         food    44.83087    -0.56762
2   Grosse Cloche de Bordeaux   place   44.83577    -0.57143
3   Pont Jacques Chaban Delmas  place   44.85866    -0.55204
4   Tour Pey-Berland            place   44.83800    -0.57771

    # Create a journai instance and display a map of your data
>>> journai = ji.Journai()
>>> journai.show_map(df)
```

<p align="center">
  <a href="#"><img src="./docs/misc/map_bdx.png" width="550"></a>
</p>

```python
    # use the clustering module to group different places
>>> df['cluster'] = journai.compute_cluster(df, nb_cluster=3)
>>> journai.show_cluster(df)
```

<p align="center">
  <a href="#"><img src="./docs/misc/cluster.png" width="550"></a>
</p>

```python
    # run the tsp solver to get the right path between those places
>>> df['tsp'] = journai.compute_tsp(df)
>>> journai.show_tsp(df)
```

<p align="center">
  <a href="#"><img src="./docs/misc/tsp.png" width="550"></a>
</p>

## Philosophy

Planning trips is an exiting time for some... and a nightmare for others.
Personnaly, I rather prefer not to plan too much my travels. I just write a list of places I will be happy to visit and... that’s it. If I fail to go somewhere, that’s fine.
However it happens that some travels are by far more chaotics than optimal...
It is in the economy of all effort that I built this tool over the years.
At first it was a wild Jupyter Notebook and it evolved into this current library.

For now, this lib has one job : to build a raw plan of your trip.

### A [Vehicle Routing Problem](https://developers.google.com/optimization/routing/vrp#distance_matrix_api) ?
In my opinion, it can be if you have an hotel booked, viewed here as the "depot".
But this particular constraint is hard and I want my trip easy and flexible.

### A [Traveling Salesman Problem](https://developers.google.com/optimization/routing/tsp) ?
It can be if you just have one day, but I would rather visit an area at a time so I would prefere to several separated planned loops.

### A [Clustering Problem](https://scikit-learn.org/stable/modules/clustering.html) ?
Here we go, clustering seems nice as it shows us adresses very close to each other, adding a tsp solver on each cluster and I think that we are good to go !

### Visual map : [Folium](https://github.com/python-visualization/folium)
What I really enjoyed during this project is its map display side.
It is a very eye pleasing thing to see clusters and tsp loops poping on the screen. It make the result quite tangible and even alive.
And instead of having a ordered list of places to visit, you can build the html format version of the map, so you can acces it through your personal website or download it localy on your smartphone or computer and open it in your favorit browser.

To sum-up, `journai` stands on shoulder of geants like Google OR Tools, Scikit Learn and Folium, to make your planning stategy even easyer to create.

## 🛠 Installation

:snake: You need to install **Python 3.10** or above.

Installation can be done by using `pip`.
There are [wheels available](https://pypi.org/project/journai/#files) for **Linux**, **MacOS**, and **Windows**.

```bash
pip install journai
```

You can also install the latest development version as so:

```bash
pip install git+https://github.com/tlentali/journai

# Or, through SSH:
pip install git+ssh://git@github.com/tlentali/journai.git
```

## ⚙️ Under the hood

You can use this [site](https://www.gps-coordinates.net/) to convert an adress to lat-lon coordinates.
This project uses machine learning and operation research tools : a **great blend**.

First, depending on the number of days you are staying, `journai` uses [Kmeans](https://scikit-learn.org/stable/modules/clustering.html#k-means) algorithm to regroup places into clusters.
Then, a [Traveling Sellsman Problem](https://developers.google.com/optimization/routing/tsp) solver comes in hand to determine the shortest path to use between places in each cluster, starting from your staying place.

## 🔥 Features

- Generate clusters of places you want to see
- Compute the TSP in each clusters
- Show the map of our global trip displaying places you want to visit, by cluster and showing the TSP path
- Data sample available for :
  - London (UK)
  - Paris (France)
  - Copenhagen (Danemark)
  - San Francisco (US)
  - New York (US)
  - Bristol (UK)
  - Jaipur (India)
  - Hanoi (Vietnam)
  - Bordeaux (France)

## 🖖 Contributing

Feel free to contribute in any way you like, we're always open to new ideas and approaches. If you want to contribute to the code base please check out the [CONTRIBUTING.md](https://github.com/tlentali/journai/blob/master/CONTRIBUTING.md) file. Also take a look at the [issue tracker](https://github.com/tlentali/journai/issues) and see if anything takes your fancy.

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Again, contributions of any kind are welcome!

## 📜 Licence

`journai` is free and open-source software licensed under the [3-clause BSD license](https://github.com/tlentali/journai/blob/master/LICENSE).
