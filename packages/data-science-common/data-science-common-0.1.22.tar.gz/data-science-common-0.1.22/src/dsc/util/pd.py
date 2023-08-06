# Standard library imports
import re
from typing import Optional

# Third party imports
import inflection
import pandas as pd
from tabulate import tabulate

# fmt: off
__all__ = [
    'tabulate_dataframe',
    'print_dataframe',
]
# fmt: on


def tabulate_dataframe(df: pd.DataFrame, nrows: Optional[int] = None) -> Optional[str]:
    """
    Creates a nicely formatted string/tables for a pandas dataframe

    Args:
        df:  the dataframe to print
        nrows: the number of rows to display
    Returns:
        formatted dataframe sting-based output
    """

    if df.empty:
        print("pandas.DataFrame has no rows")
        return None
    return tabulate(df.head(nrows), headers="keys", tablefmt="psql")


def print_dataframe(df: pd.DataFrame, nrows: Optional[int] = None) -> None:
    """
    Prints a nicely formatted table for a pandas dataframe

    Args:
        df:  the dataframe to print
        nrows: the number of rows to display
    """

    print(tabulate_dataframe(df, nrows=nrows))


def columns_to_snakecase(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the columns of the dataframe to snake case.

    Args:
        df:  the dataframe to convert
    Returns:
        dataframe snakecase columns
    """

    def replace(c: str) -> str:
        result = inflection.underscore(c)
        result = re.sub(r"\W+", "_", result)
        result = re.sub(r"\s+", "_", result)
        result = re.sub(r"(^_)|(_$)", "", result)
        return result

    columns = [replace(c) for c in df.columns]
    df.columns = columns
    return df
