from typing import List
from spotlight.core.common.base import Base


class SearchRequest(Base):
    """
    Model for search requests
    """

    query: str


class LookupRequest(Base):
    group_ids: List[str]
    group_names: List[str]
