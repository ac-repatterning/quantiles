"""Module interface.py"""
import logging
import os

import dask
import pandas as pd
import json

import config
import src.algorithms.data
import src.algorithms.metrics
import src.algorithms.persist
import src.elements.partition as prt
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix
import src.functions.objects


class Interface:
    """
    The interface to quantiles calculations.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, reference: pd.DataFrame, arguments: dict):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        :param arguments: A set of arguments vis-à-vis calculation & storage objectives.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters
        self.__reference = reference
        self.__arguments = arguments

        # Names
        self.__rename = {
            0.05: 'e_l_whisker', 0.10: 'l_whisker', 0.25: 'l_quartile', 0.5: 'median',
            0.75: 'u_quartile', 0.9: 'u_whisker', 0.95: 'e_u_whisker'}

    def __persist(self, aggregates: dict):
        """

        :param aggregates:
        :return:
        """

        frame = pd.DataFrame.from_dict(aggregates)
        frame.rename(columns=self.__rename, inplace=True)
        details = frame.merge(self.__reference, how='left', on=['catchment_id', 'ts_id'])
        details.set_index(keys='ts_id', inplace=True)

        string = details.to_json(orient='index')
        nodes = json.loads(string)
        src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(config.Config().quantiles_, 'aggregates.json'))

    def exc(self, partitions: list[prt.Partition], ):
        """

        :param partitions: The time series partitions.

        :return:
        """

        # Delayed tasks
        __data = dask.delayed(src.algorithms.data.Data(
            service=self.__service, s3_parameters=self.__s3_parameters, arguments=self.__arguments).exc)
        __metrics = dask.delayed(src.algorithms.metrics.Metrics(
            reference=self.__reference).exc)
        __persist = dask.delayed(src.algorithms.persist.Persist(
            reference=self.__reference).exc)

        computations = []
        for partition in partitions:
            data = __data(partition=partition)
            __aggregates = __metrics(data=data, partition=partition)
            computations.append(__aggregates)
        aggregates = dask.compute(computations, scheduler='threads')[0]
        logging.info(aggregates)

        self.__persist(aggregates=aggregates)
