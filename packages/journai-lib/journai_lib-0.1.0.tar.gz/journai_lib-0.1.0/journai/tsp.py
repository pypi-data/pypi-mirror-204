from sklearn.neighbors import DistanceMetric
from math import radians
import pandas as pd
import numpy as np
import logging

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from scipy.spatial import distance_matrix


class Tsp:
    """
    Build Tsp object using Google OR Tools library.

    Parameters:
        df (pd.DataFrame): Localication in Pandas DataFrame format.
        col_lat (str): Name of the latitude column.
        col_lon (str): Name of the longitude column.
        col_name (str): Name of the place name column.
    """

    def __init__(self, df, col_lat, col_lon, col_name):
        self.df = df
        self.col_lat = col_lat
        self.col_lon = col_lon
        self.col_name = col_name

    @staticmethod
    def compute_distance_matrix(df, col_lat, col_lon, col_name):
        """
        Since the routing solver does all computations with integers,
        the distance callback must return an integer distance for any two locations
        https://developers.google.com/optimization/routing/tsp#scaling
        """
        logging.debug('Building distance matrix')
        dm = pd.DataFrame(
            distance_matrix(
                df[[col_lat, col_lon]].values,
                df[[col_lat, col_lon]].values,
            ),
            index=df[col_name],
            columns=df[col_name],
        )
        return (dm * 100000).astype(int).values.tolist()

    def create_data_model(self):
        logging.debug('Stores the data for the problem.')
        data = {}
        data["distance_matrix"] = self.compute_distance_matrix(
            self.df, self.col_lat, self.col_lon, self.col_name
        )
        data["num_vehicles"] = 1
        data["depot"] = 0
        return data

    @staticmethod
    def get_solution(manager, routing, solution):
        index = routing.Start(0)
        route_distance = 0
        result = []
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            result.append(manager.IndexToNode(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        return result

    def get_tsp(self):
        """Entry point of the program."""
        logging.debug('Instantiate the data problem.')
        data = self.create_data_model()

        logging.debug('Create the routing index manager.')
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )

        logging.debug('Create Routing Model.')
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            logging.info('Convert from routing variable Index to distance matrix NodeIndex.')
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 1
        search_parameters.log_search = True
        search_parameters.use_full_propagation = True

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        logging.debug('Define cost of each arc.')
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        logging.debug('Solve the problem.')
        solution = routing.SolveWithParameters(search_parameters)

        logging.debug('Solution.')
        return self.get_solution(manager, routing, solution)
