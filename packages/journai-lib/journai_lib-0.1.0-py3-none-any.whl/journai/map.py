import folium
import pandas as pd
import logging


class Map:
    """
    Build Map object using Folium library.

    Parameters:
        df (pd.DataFrame): Localication in Pandas DataFrame format.
        col_lat (str): Name of the latitude column.
        col_lon (str): Name of the longitude column.
        col_name (str): Name of the place name column.
    """

    TILES = "Stamen Toner"
    CLUSTER_COLOR = {
        0: "lightblue",
        1: "darkred",
        2: "lightgreen",
        3: "cadetblue",
        4: "pink",
        5: "darkgreen",
        6: "beige",
        7: "darkpurple",
        8: "lightred",
        9: "purple",
        10: "red",
        11: "blue",
        12: "gray",
        13: "green",
        14: "darkblue",
        15: "orange",
        16: "lightgray",
        17: "black",
    }

    def __init__(self, df: pd.DataFrame, col_lat: str, col_lon: str, col_name: str):
        self.df = df
        self.col_lat = col_lat
        self.col_lon = col_lon
        self.col_name = col_name
        self.col_cluster = None
        self.lat_lon = None
        self.df_cluster = None
        self.map = None

    def show_map(self):
        self.build_map(self.df)
        self.add_point(self.df)
        return self.map

    def show_cluster(self, col_cluster):
        self.build_map(self.df)
        self.col_cluster = col_cluster
        self.add_clusters(self.df)
        return self.map

    def build_map(self, df) -> None:
        self.map = folium.Map(location=self.get_center_point(df), tiles=self.TILES)
        self.set_zoom_level(df)

    def get_center_point(self, df) -> None:
        """
        Get the point to centerthe map.
        """
        return [
            df[[self.col_lat, self.col_lon]].mean()[0],
            df[[self.col_lat, self.col_lon]].mean()[1],
        ]

    def set_zoom_level(self, df) -> None:
        """
        Set the right zoom level.
        """
        self.map.fit_bounds(self.get_zoom_level(df))

    def get_zoom_level(self, df) -> list:
        """
        Get the best zoom level.
        """
        south_west = df[[self.col_lat, self.col_lon]].min().values.tolist()
        north_east = df[[self.col_lat, self.col_lon]].max().values.tolist()
        return [south_west, north_east]

    def add_point(self, df) -> None:
        """
        Add point to the map.
        """
        lat_lon = self.extract_lat_lon(df)
        for point in range(0, len(lat_lon)):
            folium.Marker(lat_lon[point], popup=df[self.col_name][point]).add_to(
                self.map
            )

    def extract_lat_lon(self, df) -> list:
        """
        Isolate lat/lon columns from DataFrame.
        """
        return df[[self.col_lat, self.col_lon]].values.tolist()

    def add_clusters(self, df) -> None:
        lat_lon = self.extract_lat_lon(df)
        for point in range(0, len(lat_lon)):
            folium.Marker(
                lat_lon[point],
                icon=folium.Icon(
                    # we add modulo 16 because we have only 16 colors allowed in folium
                    color=self.CLUSTER_COLOR[
                        self.df.iloc[point][self.col_cluster] % 16
                    ],
                    icon="far fa-compass",
                    prefix="fa",  # needed for icon from flavicon
                ),
                popup=df[self.col_name][point],
            ).add_to(self.map)

    def show_tsp(self, col_cluster: str = "cluster", col_tsp: str = "tsp"):
        one_cluster_map = self.show_cluster(col_cluster)
        grouped = self.df.groupby(col_cluster)
        res = []
        for _, group in grouped:
            group = group.sort_values(by=col_tsp, ascending=True)
            res.append(group)
            for df in res:
                df_close_loop_tsp = df.iloc[0].copy()
                df_close_loop_tsp[col_tsp] = df[self.col_lon].max() + 1
                df = pd.concat([df, df_close_loop_tsp.to_frame().T], ignore_index=False)
                points = list(zip(df[self.col_lat], df[self.col_lon]))
                folium.PolyLine(points, color="#f60386", weight=2.5, opacity=1).add_to(
                    one_cluster_map
                )
        return one_cluster_map
