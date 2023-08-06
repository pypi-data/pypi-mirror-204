from bc_time.api.objects.object_base_read import ObjectBaseRead
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType

class ApiAuthorisations(ObjectBaseRead):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)
        self._content_type_id = ContentType.api_authorisation

    def get_current(self) -> dict:
        return self.api.get_one(
            content_type_id=self._content_type_id,
            content_uid=None # None will result in no content ID being sent to Time's API, which will cause the results of the current API to be returned.
        )

    def get_current_api_authorisation(self) -> dict:
        """Deprecated method; will be removed in a future release."""
        return self.get_current()