from typing import Optional, List

from pydantic import Field

from data_watch.common.base import Base
from data_watch.common.enum import Severity


class RuleRequest(Base):
    name: str
    predicate: str
    description: Optional[str] = Field(default=None)
    threshold: Optional[int] = Field(default=None)
    severity: Optional[Severity] = Field(default=Severity.ERROR)
    tags: Optional[List[str]] = Field(default=None)


class RuleResponse(Base):
    id: str
    name: str
    description: Optional[str]
    predicate: str
    threshold: int
    severity: Severity
    tags: Optional[List[str]]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class RuleGroupResponse(Base):
    group_id: str
    rule_id: str
    created_by: str
    created_at: int
