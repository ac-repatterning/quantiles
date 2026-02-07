"""Module interface.py"""
import logging

import dask
import pandas as pd

import src.algorithms.data
import src.algorithms.persist
import src.algorithms.quantiles
import src.elements.partitions as pr
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix


class Interface:
    """
    The interface to quantiles calculations.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        :param arguments: A set of arguments vis-à-vis calculation & storage objectives.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    def exc(self, partitions: list[pr.Partitions], reference: pd.DataFrame):
        """

        :param partitions: The time series partitions.
        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        :return:
        """

        # Delayed tasks
        __data = dask.delayed(src.algorithms.data.Data(
            service=self.__service, s3_parameters=self.__s3_parameters, arguments=self.__arguments).exc)
        __quantiles = dask.delayed(
            src.algorithms.quantiles.Quantiles().exc)
        __persist = dask.delayed(src.algorithms.persist.Persist(reference=reference).exc)

        computations = []
        for partition in partitions:
            data = __data(partition=partition)
            quantiles = __quantiles(data=data)
            message = __persist(metrics=quantiles, partition=partition)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(messages)
