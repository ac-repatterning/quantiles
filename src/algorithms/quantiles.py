"""Module quantiles.py"""

import cudf
import numpy as np


class Quantiles:
    """
    Calculates daily quantiles per gauge
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_aggregates(data: cudf.DataFrame):

        __metrics = data['measure'].quantile(q = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95])
        metrics = __metrics.to_dict()

        sequence = data['measure'].to_numpy()
        i_minimum = np.nanargmin(sequence)
        i_maximum = np.nanargmax(sequence)

        metrics.update({
            'minimum': float(data['measure'].values[i_minimum]),
            'minimum_': float(data['timestamp'].values[i_minimum]),
            'maximum': float(data['measure'].values[i_maximum]),
            'maximum_': float(data['timestamp'].values[i_maximum])
        })

        return metrics

    def exc(self, data: cudf.DataFrame) -> cudf.DataFrame:
        """

        :param data: A data frame consisting of fields ['date', 'timestamp', 'measure'] <b>only</b>.<br>
        :return:
        """

        q010 = lambda z: z.quantile(0.10); q010.__name__ = 'l_whisker'
        q025 = lambda z: z.quantile(0.25); q025.__name__ = 'l_quartile'
        q050 = lambda z: z.quantile(0.50); q050.__name__ = 'median'
        q075 = lambda z: z.quantile(0.75); q075.__name__ = 'u_quartile'
        q090 = lambda z: z.quantile(0.90); q090.__name__ = 'u_whisker'
        frame = data[['date', 'measure']].groupby(by='date', as_index=True, axis=0).agg(
            [q010, q025, q050, q075, q090, 'min', 'max'])

        aggregates = self.__get_aggregates(data=data)
        print(aggregates)

        return frame.loc[:, 'measure']
