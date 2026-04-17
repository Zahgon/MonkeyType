# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import functools
import os
import pathlib
import sys
import sysconfig
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from types import CodeType
from typing import Iterator, Optional

from monkeytype.db.base import CallTraceStore, CallTraceStoreLogger
from monkeytype.db.sqlite import SQLiteStore
from monkeytype.tracing import CallTraceLogger, CodeFilter
from monkeytype.typing import DEFAULT_REWRITER, NoOpRewriter, TypeRewriter


class Config(metaclass=ABCMeta):
    """A Config ties together concrete implementations of the different abstractions
    that make up a typical deployment of MonkeyType.
    """

    @abstractmethod
    def trace_store(self) -> CallTraceStore:
        """Return the CallTraceStore for storage/retrieval of call traces."""
        pass

    @contextmanager
    def cli_context(self, command: str) -> Iterator[None]:
        """Lifecycle hook that is called once right after the CLI
        starts.

        `command` is the name of the command passed to monkeytype
        ('run', 'apply', etc).
        """
        pass

    def trace_logger(self) -> CallTraceLogger:
        """Return the CallTraceLogger for logging call traces.

        By default, returns a CallTraceStoreLogger that logs to the configured
        trace store.
        """
        pass

    def code_filter(self) -> Optional[CodeFilter]:
        """Return the (optional) CodeFilter predicate for triaging calls.

        A CodeFilter is a callable that takes a code object and returns a
        boolean determining whether the call should be traced or not. If None is
        returned, all calls will be traced and logged.
        """
        pass

    def sample_rate(self) -> Optional[int]:
        """Return the sample rate for call tracing.

        By default, all calls will be traced. If an integer sample rate of N is
        set, 1/N calls will be traced.
        """
        pass

    def type_rewriter(self) -> TypeRewriter:
        """Return the type rewriter for use when generating stubs."""
        pass

    def query_limit(self) -> int:
        """Maximum number of traces to query from the call trace store."""
        pass

    def max_typed_dict_size(self) -> int:
        """Size up to which a dictionary will be traced as a TypedDict."""
        pass


lib_paths = {sysconfig.get_path(n) for n in ["stdlib", "purelib", "platlib"]}
# if in a virtualenv, also exclude the real stdlib location
venv_real_prefix = getattr(sys, "real_prefix", None)
if venv_real_prefix:
    lib_paths.add(
        sysconfig.get_path("stdlib", vars={"installed_base": venv_real_prefix})
    )
LIB_PATHS = tuple(pathlib.Path(p).resolve() for p in lib_paths if p is not None)


def _startswith(a: pathlib.Path, b: pathlib.Path) -> bool:
    pass


@functools.lru_cache(maxsize=8192)
def default_code_filter(code: CodeType) -> bool:
    """A CodeFilter to exclude stdlib and site-packages."""
    pass


class DefaultConfig(Config):
    DB_PATH_VAR = "MT_DB_PATH"

    def type_rewriter(self) -> TypeRewriter:
        pass

    def trace_store(self) -> CallTraceStore:
        """By default we store traces in a local SQLite database.

        The path to this database file can be customized via the `MT_DB_PATH`
        environment variable.
        """
        pass

    def code_filter(self) -> CodeFilter:
        """Default code filter excludes standard library & site-packages."""
        pass


def get_default_config() -> Config:
    """Use monkeytype_config.CONFIG if it exists, otherwise DefaultConfig().

    monkeytype_config is not a module that is part of the monkeytype
    distribution, it must be created by the user.
    """
    pass
