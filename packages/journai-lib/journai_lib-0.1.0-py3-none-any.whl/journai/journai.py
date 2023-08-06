import pandas as pd
import logging

from dataclasses import dataclass
from journai.cluster import Cluster
from journai.tsp import Tsp
from journai.map import Map

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


class Journai:
    """
    Build Journai object using Cluster, Tsp and Map.
    """

    def __init__(self):
        pass

    def compute_cluster(
        self,
        df: pd.DataFrame,
        nb_cluster: int = 5,
        col_lat: str = "lat",
        col_lon: str = "lon",
    ):
        cluster = Cluster(df, col_lat, col_lon)
        return cluster.get_clusters(nb_cluster, "cluster")

    def compute_tsp(
        self,
        df: pd.DataFrame,
        col_cluster: str = "cluster",
        col_lat: str = "lat",
        col_lon: str = "lon",
        col_name: str = "name",
    ):
        tsp_group = df.groupby(col_cluster).apply(
            lambda x: Tsp(x, col_lat, col_lon, col_name).get_tsp()
        )
        logging.debug('Tsp groups done')

        for cluster_nb in tsp_group.index:
            logging.debug(f'{cluster_nb} in process')

            tsp_res = tsp_group.iloc[cluster_nb]
            tsp_res = pd.DataFrame(tsp_res, columns=["tsp"])
            tsp_res = tsp_res.sort_values(by="tsp")
            tsp_res = tsp_res.reset_index()
            res = tsp_res["index"].tolist()
            df.loc[df[col_cluster] == cluster_nb, "tsp"] = res
        return df["tsp"]

    def show_map(
        self,
        df: pd.DataFrame,
        col_lat: str = "lat",
        col_lon: str = "lon",
        col_name: str = "name",
    ):
        return Map(df, col_lat=col_lat, col_lon=col_lon, col_name=col_name).show_map()

    def show_clusters(
        self,
        df: pd.DataFrame,
        col_cluster="cluster",
        col_lat: str = "lat",
        col_lon: str = "lon",
        col_name: str = "name",
    ):
        return Map(
            df, col_lat=col_lat, col_lon=col_lon, col_name=col_name
        ).show_cluster(col_cluster=col_cluster)

    def show_tsp(
        self,
        df: pd.DataFrame,
        col_lat: str = "lat",
        col_lon: str = "lon",
        col_name: str = "name",
        col_cluster: str = "cluster",
        col_tsp: str = "tsp",
    ):
        return Map(df, col_lat=col_lat, col_lon=col_lon, col_name=col_name).show_tsp(
            col_cluster=col_cluster, col_tsp=col_tsp
        )
