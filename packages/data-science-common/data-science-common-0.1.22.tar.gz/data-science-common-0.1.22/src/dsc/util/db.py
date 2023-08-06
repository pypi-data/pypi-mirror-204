# Standard library imports
from typing import Any, Dict, Optional, Union

# Third party imports
import pandas as pd
import sqlparse
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Selectable

# DSC imports
from dsc.util.pd import print_dataframe

# fmt: off
__all__ = [
    "RunQuery"
]
# fmt: on


class RunQuery(object):
    """
        Wrapper to run a SQL from pandas so that the engine is encapsulated.

        This is to alleviate constantly passing in the engine. For Example:

    .. highlight:: python
    .. code-block:: python

        engine = create_engine("sqlite://")
        run_sql = RunQuery(engine)
        df1 = run_sql("select 1 as foo")
        df2 = run_sql("select 2 as foo")

    """

    def __init__(self, engine: Engine):
        """
        Constructor

        Args:
            engine (Engine): SQLALCHEMY engine to run queries against
        """
        self.engine = engine

    def __call__(
        self,
        query: Union[str, Selectable],
        parameters: Optional[Dict[Any, Any]] = None,
        verbose: bool = False,
        display: bool = False,
    ) -> pd.DataFrame:
        """
        Execute a query.

        Args:
            query (str or SQLAlchemy selectable): query to run
            parameters (Optional[dict]): dictionary of parameters to pass to query
            verbose (bool): show the query
            display (bool): show the first few rows of the result

        Returns:
            pd.DataFrame with the query result
        """

        try:
            if verbose:
                if isinstance(query, Selectable):
                    query_str = str(
                        query.compile(
                            self.engine, compile_kwargs={"literal_binds": True}
                        )
                    )
                    query_str_fmt = sqlparse.format(
                        query_str,
                        reindent=True,
                        keyword_case="lower",
                        identifier_case="lower",
                    )
                    print(query_str_fmt)
                else:
                    print(query)
            df = pd.read_sql_query(sql=query, con=self.engine, params=parameters)
            if display:
                # Standard library imports
                import sys

                # Third party imports
                from IPython.display import display as ipy_display

                if "ipykernel" in sys.modules:
                    # noinspection PyTypeChecker
                    ipy_display(df.head(3))
                else:
                    print_dataframe(df, 3)
            return df
        except Exception as e:
            print(e)
            raise e
