"""Module quantiles.py"""

import cudf


class Quantiles:
    """
    Calculates daily quantiles per gauge
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(data: cudf.DataFrame) -> cudf.DataFrame:
        """

        :param data: A data frame consisting of fields ['date', 'measure'] <b>only</b>.<br>
        :return:
        """

        q010 = lambda z: z.quantile(0.10); q010.__name__ = 'l_whisker'
        q025 = lambda z: z.quantile(0.25); q025.__name__ = 'l_quartile'
        q050 = lambda z: z.quantile(0.50); q050.__name__ = 'median'
        q075 = lambda z: z.quantile(0.75); q075.__name__ = 'u_quartile'
        q090 = lambda z: z.quantile(0.90); q090.__name__ = 'u_whisker'
        x = data.groupby(by='date', as_index=True, axis=0).agg([q010, q025, q050, q075, q090, 'min', 'max'])

        return x.loc[:, 'measure']
