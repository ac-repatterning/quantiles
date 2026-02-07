"""Module persist.py"""
import json
import os

import cudf
import pandas as pd

import config
import src.elements.partition as prt
import src.functions.objects


class Persist:
    """
    Persist
    """

    def __init__(self, reference: pd.DataFrame):
        """

        :param reference: A reference of gauges, and their attributes.
        """

        self.__reference = reference

        self.__configurations = config.Config()

        self.__objects = src.functions.objects.Objects()

    def __get_nodes(self, data: cudf.DataFrame, ts_id: int) -> dict:
        """

        :param data: Quantiles
        :param ts_id: A time series identification code
        :return:
        """

        attributes: pd.Series = self.__reference.loc[self.__reference['ts_id'] == ts_id, :].squeeze()

        string = data.to_pandas().to_json(orient='split')
        nodes = json.loads(string)
        nodes.update(attributes.to_dict())

        return nodes

    def exc(self, disaggregates: cudf.DataFrame, partition: prt.Partition) -> str:

        metrics = disaggregates.copy().rename(columns={'min': 'minimum', 'max': 'maximum'})
        frame = metrics.reset_index(drop=False)

        # Ascertain date order
        data = frame.sort_values(by='date', ascending=True, ignore_index=True)

        # The nodes
        nodes = self.__get_nodes(data=data, ts_id=partition.ts_id)

        # Write
        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.points_, f'{partition.ts_id}.json'))

        return message
