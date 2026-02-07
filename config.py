"""Module config.py"""
import os


class Config:
    """
    Class Config

    For project settings
    """

    def __init__(self):
        """
        Constructor
        """

        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')
        self.quantiles_ = os.path.join(self.warehouse, 'quantiles')
        self.points_ = os.path.join(self.quantiles_, 'points')
        self.menu_ = os.path.join(self.quantiles_, 'menu')

        # Keys
        self.s3_parameters_key = 's3_parameters.yaml'
        self.arguments_key = 'quantiles/arguments.json'
        self.metadata_ = 'quantiles/external'

        # The prefix of the Amazon repository where the quantiles will be stored
        self.prefix = 'warehouse/quantiles'
