"""Module gauges.py"""
import numpy as np
import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix


class Gauges:
    """
    Retrieves the catchment & time series codes of the gauges in focus.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param service:
        :param s3_parameters:
        :param arguments:
        """

        self.__service = service
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

        # An instance for interacting with objects within an Amazon S3 prefix
        self.__pre = src.s3.prefix.Prefix(
            service=self.__service,
            bucket_name=self.__s3_parameters._asdict()[arguments['s3']['p_bucket']])

    @staticmethod
    def __get_elements(objects: list[str], prefixes: list[str]) -> pd.DataFrame:
        """

        :param objects:
        :return:
        """

        # A set of S3 uniform resource locators
        strings = [i.rsplit('/', 1)[0] for i in objects]
        values = pd.DataFrame(data={'uri': objects, 'prefix': prefixes, 'string': strings})

        # Splitting locators
        rename = {0: 'endpoint', 1: 'catchment_id', 2: 'ts_id'}
        splittings = values['string'].str.rsplit('/', n=2, expand=True)
        splittings.rename(columns=rename, inplace=True)

        # Collating
        values = values.copy().join(splittings, how='left')

        return values

    def __get_prefixes(self) -> list[str]:
        """

        :return:
        """

        paths = self.__pre.objects(
            prefix=(self.__s3_parameters._asdict()[self.__arguments['s3']['p_prefix']]
                    + f"{self.__arguments['s3']['affix']}/"),
            delimiter='/')

        computations = []
        for path in paths:
            listings = self.__pre.objects(prefix=path, delimiter='/')
            computations.append(listings)
        prefixes: list[str] = sum(computations, [])

        return prefixes

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        prefixes = self.__get_prefixes()
        if len(prefixes) > 0:
            objects = [f's3://{self.__s3_parameters.internal}/{prefix}' for prefix in prefixes]
        else:
            return pd.DataFrame()

        # The variable objects is a list of uniform resource locators.  Each locator includes a 'ts_id',
        # 'catchment_id', 'datestr' substring; the function __get_elements extracts these items.
        values = self.__get_elements(objects=objects, prefixes=prefixes)

        # Types
        values['catchment_id'] = values['catchment_id'].astype(dtype=np.int64)
        values['ts_id'] = values['ts_id'].astype(dtype=np.int64)
        values.drop(columns=['endpoint', 'string'], inplace=True)

        return values
