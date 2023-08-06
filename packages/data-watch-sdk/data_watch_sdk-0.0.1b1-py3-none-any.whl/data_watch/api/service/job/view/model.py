from typing import Optional, List

from data_watch.api.service.group.model import GroupResponse
from data_watch.common.base import Base
from data_watch.common.enum import Status


class JobViewResponse(Base):
    id: str
    name: str
    status: Status
    groups: List[GroupResponse]
    start_time: Optional[int]
    end_time: Optional[int]
    metadata: dict
    tags: List[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
