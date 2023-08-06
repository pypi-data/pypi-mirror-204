from typing import Optional, List

from pydantic import Field

from data_watch.common.base import Base
from data_watch.common.enum import Status


class JobRequest(Base):
    name: str
    status: Status
    group_ids: Optional[List[str]] = Field(default=None)
    start_time: Optional[int] = Field(default=None)
    end_time: Optional[int] = Field(default=None)
    metadata: Optional[dict] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)


class JobResponse(Base):
    id: str
    name: str
    status: Status
    start_time: Optional[int]
    end_time: Optional[int]
    metadata: dict
    tags: List[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class JobGroupResponse(Base):
    group_id: str
    rule_id: str
    created_by: str
    created_at: int
