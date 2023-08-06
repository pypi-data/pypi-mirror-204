from typing import Any, Dict, List, Optional, Tuple

from shillelagh.backends.apsw.dialects.base import APSWDialect
from sqlalchemy.engine import Connection
from sqlalchemy.engine.url import URL

# -----------------------------------------------------------------------------

ADAPTER_NAME = "system"


# -----------------------------------------------------------------------------


class SystemDialect(APSWDialect):
    supports_statement_cache = True

    def __init__(
            self,
            **kwargs: Any,
    ):
        # We tell Shillelagh that this dialect supports just one adapter
        super().__init__(safe=True, adapters=[ADAPTER_NAME], **kwargs)

    def get_table_names(
            self, connection, schema=None, sqlite_include_internal=False, **kw
    ) -> List[str]:
        return ["system"]


