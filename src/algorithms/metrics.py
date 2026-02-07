"""Module metrics.py"""

import cudf
import numpy as np
import pandas as pd

import src.algorithms.persist
import src.elements.partition as prt


class Metrics:
    """
    Calculates daily quantiles per gauge
    """

    def __init__(self,  reference: pd.DataFrame):

        self.__persist = src.algorithms.persist.Persist(reference=reference)

    @staticmethod
    def __get_aggregates(data: cudf.DataFrame, partition: prt.Partition):

        values = data['measure'].quantile(q = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95])
        aggregates = values.to_dict()

        sequence = data['measure'].to_numpy()
        i_minimum = np.nanargmin(sequence)
        i_maximum = np.nanargmax(sequence)

        aggregates.update({
            'minimum': float(data['measure'].values[i_minimum]),
            'minimum_': float(data['timestamp'].values[i_minimum]),
            'maximum': float(data['measure'].values[i_maximum]),
            'maximum_': float(data['timestamp'].values[i_maximum]),
            'ts_id': partition.ts_id,
            'catchment_id': partition.catchment_id
        })

        return aggregates

    def exc(self, data: cudf.DataFrame, partition: prt.Partition) -> dict:
        """

        :param data: A data frame consisting of fields ['date', 'timestamp', 'measure'] <b>only</b>.<br>
        :param partition
        :return:
        """

        q010 = lambda z: z.quantile(0.10); q010.__name__ = 'l_whisker'
        q025 = lambda z: z.quantile(0.25); q025.__name__ = 'l_quartile'
        q050 = lambda z: z.quantile(0.50); q050.__name__ = 'median'
        q075 = lambda z: z.quantile(0.75); q075.__name__ = 'u_quartile'
        q090 = lambda z: z.quantile(0.90); q090.__name__ = 'u_whisker'
        frame = data[['date', 'measure']].groupby(by='date', as_index=True, axis=0).agg(
            [q010, q025, q050, q075, q090, 'min', 'max'])
        self.__persist.exc(disaggregates=frame.loc[:, 'measure'], partition=partition)

        aggregates = self.__get_aggregates(data=data, partition=partition)

        return aggregates
