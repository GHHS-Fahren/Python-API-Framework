"""
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
       This code is out of date! Do not use for the time being!       
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
"""

from __future__ import annotations

from .business.models import BusinessRequest, BusinessResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.api.gohighlevel.api_client import GHLClient
    from collections.abc import Iterator



class BusinessRecordApi():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def search_businesses(
        self,
        page: int = 1,
        limit: int = 20,
        q
    )