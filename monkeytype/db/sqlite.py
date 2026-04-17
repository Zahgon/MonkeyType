# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import datetime
import logging
import sqlite3
from typing import Iterable, List, Optional, Tuple, Union

from monkeytype.db.base import CallTraceStore, CallTraceThunk
from monkeytype.encoding import CallTraceRow, serialize_traces
from monkeytype.tracing import CallTrace

logger = logging.getLogger(__name__)


DEFAULT_TABLE = "monkeytype_call_traces"


def create_call_trace_table(
    conn: sqlite3.Connection, table: str = DEFAULT_TABLE
) -> None:
    pass


QueryValue = Union[str, int]
ParameterizedQuery = Tuple[str, List[QueryValue]]


def make_query(
    table: str, module: str, qualname: Optional[str], limit: int
) -> ParameterizedQuery:
    pass


class SQLiteStore(CallTraceStore):
    def __init__(self, conn: sqlite3.Connection, table: str = DEFAULT_TABLE) -> None:
        self.conn = conn
        self.table = table

    @classmethod
    def make_store(cls, connection_string: str) -> "CallTraceStore":
        pass

    def add(self, traces: Iterable[CallTrace]) -> None:
        values = []
        for row in serialize_traces(traces):
            values.append(
                (
                    datetime.datetime.now(),
                    row.module,
                    row.qualname,
                    row.arg_types,
                    row.return_type,
                    row.yield_type,
                )
            )
        with self.conn:
            self.conn.executemany(
                "INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)".format(
                    table=self.table
                ),
                values,
            )

    def filter(
        self, module: str, qualname_prefix: Optional[str] = None, limit: int = 2000
    ) -> List[CallTraceThunk]:
        pass

    def list_modules(self) -> List[str]:
        pass
