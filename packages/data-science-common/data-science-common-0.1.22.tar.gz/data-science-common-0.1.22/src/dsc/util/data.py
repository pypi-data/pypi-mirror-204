# Standard library imports
from typing import Any, Iterable

# Third party imports
import numpy

# fmt: off
__all__ = [
    "list_contains_type",
]
# fmt: on


def list_contains_type(
    values: Iterable[Any], test_type: type, require_non_empty: bool = False
) -> bool:
    """
    Determine if a list contains the given type.

    Args:
        values: list or numpy array to test
        test_type: python type to test
        require_non_empty: True: empty list returns False, False: empty list returns True (default)

    Returns:
        boolean
    """

    values = list(values)

    result = isinstance(values, Iterable) and all(
        isinstance(i, test_type) for i in values
    )
    if require_non_empty:
        result = result and len(list(values)) > 0
    return result
