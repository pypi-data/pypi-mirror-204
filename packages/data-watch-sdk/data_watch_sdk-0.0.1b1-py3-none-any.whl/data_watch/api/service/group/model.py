from typing import Optional, List

from data_watch.common.base import Base


class GroupRequest(Base):
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class GroupResponse(Base):
    id: str
    name: str
    description: Optional[str]
    tags: Optional[List[str]]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
