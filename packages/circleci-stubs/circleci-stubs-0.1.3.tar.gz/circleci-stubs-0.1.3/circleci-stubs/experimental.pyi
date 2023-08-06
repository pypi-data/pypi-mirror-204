from circleci.api import Api as Api

class Experimental(Api):
    def retry_no_cache(self, username, project, build_num, vcs_type: str = ...): ...
