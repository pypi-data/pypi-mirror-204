from bc_time.api.objects.object_base_read import ObjectBaseRead
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType

class PeriodOvertimeData(ObjectBaseRead):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)
        self._content_type_id = ContentType.period_overtime_data