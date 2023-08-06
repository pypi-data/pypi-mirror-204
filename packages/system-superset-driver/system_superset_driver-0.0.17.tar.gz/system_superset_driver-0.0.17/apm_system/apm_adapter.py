"""
An adapter for retrieving information on running processes and system utilization (CPU,
memory, disks, network, sensors).

See https://github.com/giampaolo/psutil for more information.
"""
import logging
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import psutil
import requests

from shillelagh.adapters.base import Adapter
from shillelagh.exceptions import ProgrammingError
from shillelagh.fields import DateTime, Field, Float, Order, Integer
from shillelagh.filters import Filter
from shillelagh.typing import RequestedOrder, Row

_logger = logging.getLogger(__name__)

AVERAGE_NUMBER_OF_ROWS = 100


class SystemAPI(Adapter):
    """
    An adapter for retrieving system information.
    """

    safe = False

    supports_limit = True
    supports_offset = True

    @staticmethod
    def supports(uri: str, fast: bool = True, **kwargs: Any) -> Optional[bool]:
        return True

    @staticmethod
    def parse_uri(uri: str) -> str:
        return uri

    def __init__(self, uri: str):
        super().__init__()

        print("初始化我了system")
        parsed = urllib.parse.urlparse(uri)
        self._set_columns()

    def _set_columns(self) -> None:
        self.columns: Dict[str, Field] = {
            "timestamp": DateTime(filters=None, order=Order.ASCENDING, exact=False),
            "value": Integer(filters=None,
                             order=Order.NONE,
                             exact=False, )
        }

    def get_columns(self) -> Dict[str, Field]:
        return self.columns

    def get_data(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs: Any,
    ) -> Iterator[Row]:
        url = "https://portal-apm-bemsdev-cluster01.axa-dev.wise-paas.top/api-apm/api/v1/hist/raw/data"
        params = {
            "sensors": [
                {
                    "nodeId": 8600,
                    "sensorType": "UsageAnalysis",
                    "sensorName": "Yearly 电_EC"
                }
            ],
            "startTs": "2012-12-31T16:00:00.000Z",
            "endTs": "2022-12-31T16:00:00.000Z",
            "count": 9999,
            "retTsType": "unixTs"
        }
        cookies = "_ga=GA1.1.301961310.1667954999; _ga_YFKNQX5E65=GS1.1.1682314929.485.1.1682316294.0.0.0; EIName=admin; EIToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudHJ5IjoiIiwiY3JlYXRpb25UaW1lIjoxNjgyMzI1NTM3LCJleHAiOjE2ODIzMjkxMzcsImZpcnN0TmFtZSI6ImFkbWluIiwiaWF0IjoxNjgyMzI1NTM3LCJpZCI6IjEyMDA2NGZiLTYxNDctNGY1MS05OGEwLTg5MjI0NGIwZGI1NiIsImlzcyI6Indpc2UtcGFhcyIsImxhc3RNb2RpZmllZFRpbWUiOjE2Njk3MDQ1MTIsImxhc3ROYW1lIjoiYWRtaW4iLCJyZWZyZXNoVG9rZW4iOiJkZTgyYjE4Yi1hY2QyLTQxZGEtYjQwNy1lOTQxNjg0NTE1NTkiLCJzdGF0dXMiOiIiLCJ1c2VybmFtZSI6ImFkbWluQGFkdmFudGVjaC5jb20uY24ifQ.QEX75Y5jYLUvg1GLylN-3yG-cyH8yaaS4m3sdBO3bPI"
        response = requests.post(url, json=params, cookies=cookies)
        payload = response.json()
        for record in payload:
            for value in record['value']:
                yield {
                    "timestamp": value['ts'],
                    "value": value['v']
                }
