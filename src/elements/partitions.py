"""Module partitions.py"""
import typing


class Partitions(typing.NamedTuple):
    """
    The data type class ⇾ Partitions<br><br>

    Attributes<br>
    ----------<br>
    <b>uri</b>: str<br>
        A uniform resource locator.<br><br>
    <b>prefix</b>: str<br>
        An Amazon S3 (Simple Storage Service) prefix.<br><br>
    <b>catchment_id</b>: int<br>
        The identification code of a catchment area.<br><br>
    <b>ts_id</b>: int<br>
        The identification code of a time series.<br><br>
    """
    uri: str
    prefix: str
    catchment_id: int
    ts_id: int
