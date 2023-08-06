import pandas as pd
from sklearn.cluster import KMeans


class Cluster:
    """
    Build Cluster object using Scikit Learn KMeams model.

    Parameters:
        df (pd.DataFrame): Localication in Pandas DataFrame format.
        col_lat (str): Name of the latitude column.
        col_lon (str): Name of the longitude column.
    """

    RANDOM_STATE = 42

    def __init__(self, df: pd.DataFrame, col_lat: str, col_lon: str):
        self.df = df
        self.col_lat = col_lat
        self.col_lon = col_lon

    def get_clusters(
        self, nb_clusters: int = 5, col_cluster: str = "cluster"
    ) -> pd.DataFrame:
        X = self._set_X(self.df, self.col_lat, self.col_lon)
        kmeans = self._build_clustering(nb_clusters)
        return self._get_clustering_label(kmeans, X)

    @staticmethod
    def _set_X(df: pd.DataFrame, col_lat: str, col_lon: str) -> pd.DataFrame:
        """
        Filter on lat/lon columns.
        """
        return df[[col_lon, col_lat]]

    def _build_clustering(self, nb_clusters: int = 5):
        """
        Use a kmeans algorithm to cluster each places.
        """
        return KMeans(n_clusters=nb_clusters, n_init=50, random_state=self.RANDOM_STATE)

    @staticmethod
    def _get_clustering_label(algorithm, X):
        """
        Computer clustering and return correponding labal for each row
        """
        return algorithm.fit(X).labels_
