from typing import Optional, List

from data_watch.api.service.rule.model import RuleResponse
from data_watch.common.base import Base


class GroupViewResponse(Base):
    id: str
    name: str
    description: Optional[str]
    tags: Optional[List[str]]
    rules: List[RuleResponse]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
