"""Module data.py"""

import cudf

import src.elements.partition as prt
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix


class Data:
    """
    Data
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

        # An instance for interacting with objects within an Amazon S3 prefix
        self.__bucket_name = self.__s3_parameters._asdict()[self.__arguments['s3']['p_bucket']]
        self.__pre = src.s3.prefix.Prefix(
            service=self.__service,
            bucket_name=self.__bucket_name)

    def exc(self, partition: prt.Partition) -> cudf.DataFrame:
        """

        OR
        --

        block = cudf.read_csv(partition.uri + '*.csv', usecols=['timestamp', 'measure'], compression=None)

        :param partition: Refer to src.elements.partitions
        :return:
        """

        listings = self.__pre.objects(prefix=partition.prefix.rstrip('/'))
        keys = [f's3://{self.__bucket_name}/{listing}' for listing in listings]

        blocks = [cudf.read_csv(filepath_or_buffer=key, header=0, usecols=['timestamp', 'measure'], compression=None)
                  for key in keys]
        block = cudf.concat(blocks)

        block['datestr'] = cudf.to_datetime(block['timestamp'], unit='ms')
        block['date'] = block['datestr'].dt.strftime('%Y-%m-%d')
        block['date'] = cudf.to_datetime(block['date'])

        return block[['date', 'timestamp', 'measure']]
