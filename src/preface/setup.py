"""
Module setup.py
"""
import sys

import config
import src.functions.directories
import src.s3.bucket


class Setup:
    """

    Notes
    -----

    This class prepares the Amazon S3 (Simple Storage Service) and local data environments.
    """

    def __init__(self):
        """

        Constructor
        """

        # Configurations
        self.__configurations = config.Config()

    def __local(self) -> bool:
        """

        :return:
        """

        # An instance for interacting with local directories
        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.__configurations.warehouse)

        states = [
            directories.create(p)
            for p in [self.__configurations.menu_, self.__configurations.points_, self.__configurations.aggregates_]]

        return all(states)

    def exc(self) -> bool:
        """

        :return:
        """

        if self.__local():
            return True

        sys.exit('Error: Set up failure.')
