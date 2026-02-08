"""Module menu.py"""
import logging
import os

import pandas as pd

import config
import src.functions.objects


class Menu:
    """
    Menu
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, reference: pd.DataFrame):
        """

        :param reference: The reference sheet of the water level gauges.
        :return:
        """

        # Sort
        excerpt = reference.copy().sort_values(by=['catchment_name', 'station_name'], ascending=True)

        # Nodes
        names = (excerpt['station_name'] + '/' + excerpt['catchment_name']).to_numpy()
        frame = pd.DataFrame(data={'desc': excerpt['ts_id'].to_numpy(),
                                   'name': names})
        nodes = frame.to_dict(orient='records')

        # Persist
        message = src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__configurations.menu_, 'menu.json'))
        logging.info('Graphing Menu ->\n%s', message)
