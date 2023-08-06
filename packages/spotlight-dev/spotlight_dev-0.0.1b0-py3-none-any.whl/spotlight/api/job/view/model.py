from typing import Optional, List

from spotlight.api.group.model import GroupResponse
from spotlight.core.common.base import Base
from spotlight.core.common.enum import Status


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
