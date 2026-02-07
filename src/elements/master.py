
import typing
import cudf

class Master(typing.NamedTuple):
    """

    The data type class ⇾ Master<br><br>

    Attributes<br>
    ----------<br>
    disaggregates:<br>
    aggregates:<br>
    """

    disaggregates: cudf.DataFrame
    aggregates: dict
