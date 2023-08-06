# Standard library imports
from typing import Union

# Third party imports
import sqlparse
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Selectable

# fmt: off
__all__ = [
    "compiled_query",
    "print_compiled_query"
]
# fmt: on


def _format_sql(sql: str) -> str:
    fmt_sql = str(
        sqlparse.format(
            sql, reindent=True, keyword_case="lower", identifier_case="lower"
        )
    )
    return fmt_sql


def compiled_query(engine: Engine, expr: Selectable) -> str:
    """
    Compile the query from a Selectable

    Args:
        engine: Engine to compile with
        expr: Expression to compile with

    Returns:
        string representation of the query

    """
    if hasattr(engine, "schema_for_object"):
        map = engine.schema_for_object.map_
        result = expr.compile(
            engine, compile_kwargs={"literal_binds": True}, schema_translate_map=map
        )
    else:
        result = expr.compile(engine, compile_kwargs={"literal_binds": True})

    return str(result)


def print_compiled_query(engine: Engine, expr: Union[Selectable, str]) -> None:
    """
    Print the query from a Selectable/String

    Args:
        engine: Engine to compile with
        expr: Expression to compile with
    """
    if isinstance(expr, str):
        print(expr)
    else:
        query = str(compiled_query(engine, expr))
        print(_format_sql(query))
