from _typeshed import Incomplete
from circleci.api import Api as Api

class SDK:
    apiclient: Incomplete
    logger: Incomplete
    def __init__(self, apiclient: Api, logger: Incomplete | None = ...) -> None: ...
    def build_singleton(self, username, project, vcs_type: str = ...): ...
