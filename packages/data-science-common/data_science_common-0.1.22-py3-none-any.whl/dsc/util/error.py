# fmt: off
__all__ = [
    "MissingColumnsError",
    "NoDataError",
    "InvalidArgumentError",
    "DatabaseError"
]
# fmt: on


class MissingColumnsError(RuntimeError):
    pass


class NoDataError(RuntimeError):
    pass


class InvalidArgumentError(RuntimeError):
    pass


class DatabaseError(RuntimeError):
    pass
