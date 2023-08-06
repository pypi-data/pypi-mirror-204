from _typeshed import Incomplete

class CircleCIException(Exception):
    argument: Incomplete
    message: Incomplete
    def __init__(self, argument) -> None: ...

class BadVerbError(CircleCIException):
    message: str
    def __init__(self, argument) -> None: ...

class BadKeyError(CircleCIException):
    message: str
    def __init__(self, argument) -> None: ...

class InvalidFilterError(CircleCIException):
    filter_message: str
    artifacts_message: str
    message: Incomplete
    def __init__(self, argument, filter_type) -> None: ...
