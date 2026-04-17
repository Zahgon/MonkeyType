# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import inspect
import logging
import opcode
import random
import sys
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from types import CodeType, FrameType
from typing import Any, Callable, Dict, Iterator, Optional, Union, cast

from monkeytype.compat import cached_property
from monkeytype.typing import get_type
from monkeytype.util import get_func_fqname

logger = logging.getLogger(__name__)


class CallTrace:
    """CallTrace contains the types observed during a single invocation of a function"""

    def __init__(
        self,
        func: Callable[..., Any],
        arg_types: Dict[str, type],
        return_type: Optional[type] = None,
        yield_type: Optional[type] = None,
    ) -> None:
        """
        Args:
            func: The function where the trace occurred
            arg_types: The collected argument types
            return_type: The collected return type. This will be None if the called function returns
                due to an unhandled exception. It will be NoneType if the function returns the value None.
            yield_type: The collected yield type. This will be None if the called function never
                yields. It will be NoneType if the function yields the value None.
        """
        self.func = func
        self.arg_types = arg_types
        self.return_type = return_type
        self.yield_type = yield_type

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self) -> str:
        return "CallTrace(%s, %s, %s, %s)" % (
            self.func,
            self.arg_types,
            self.return_type,
            self.yield_type,
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.func,
                frozenset(self.arg_types.items()),
                self.return_type,
                self.yield_type,
            )
        )

    def add_yield_type(self, typ: type) -> None:
        pass

    @property
    def funcname(self) -> str:
        pass


class CallTraceLogger(metaclass=ABCMeta):
    """Log and store/print records collected by a CallTracer."""

    @abstractmethod
    def log(self, trace: CallTrace) -> None:
        """Log a single call trace."""
        pass

    def flush(self) -> None:
        """Flush all logged traces to output / database.

        Not an abstractmethod because it's OK to leave it as a no-op; for very
        simple loggers it may not be necessary to batch-flush traces, and `log`
        can handle everything.
        """
        pass


def get_func_in_mro(obj: Any, code: CodeType) -> Optional[Callable[..., Any]]:
    """Attempt to find a function in a side-effect free way.

    This looks in obj's mro manually and does not invoke any descriptors.
    """
    pass


def _has_code(
    func: Optional[Callable[..., Any]], code: CodeType
) -> Optional[Callable[..., Any]]:
    pass


def get_previous_frames(frame: Optional[FrameType]) -> Iterator[FrameType]:
    pass


def get_locals_from_previous_frames(frame: FrameType) -> Iterator[Any]:
    pass


def get_func(frame: FrameType) -> Optional[Callable[..., Any]]:
    """Return the function whose code object corresponds to the supplied stack frame."""
    pass


RETURN_VALUE_OPCODE = opcode.opmap["RETURN_VALUE"]
YIELD_VALUE_OPCODE = opcode.opmap["YIELD_VALUE"]

# A CodeFilter is a predicate that decides whether or not a the call for the
# supplied code object should be traced.
CodeFilter = Callable[[CodeType], bool]

EVENT_CALL = "call"
EVENT_RETURN = "return"
SUPPORTED_EVENTS = {EVENT_CALL, EVENT_RETURN}


class CallTracer:
    """CallTracer captures the concrete types involved in a function invocation.

    On a per function call basis, CallTracer will record the types of arguments
    supplied, the type of the function's return value (if any), and the types
    of values yielded by the function (if any). It emits a CallTrace object
    that contains the captured types when the function returns.

    Use it like so:

        sys.setprofile(CallTracer(MyCallLogger()))

    """

    def __init__(
        self,
        logger: CallTraceLogger,
        max_typed_dict_size: int,
        code_filter: Optional[CodeFilter] = None,
        sample_rate: Optional[int] = None,
    ) -> None:
        self.logger = logger
        self.traces: Dict[FrameType, CallTrace] = {}
        self.sample_rate = sample_rate
        self.cache: Dict[CodeType, Optional[Callable[..., Any]]] = {}
        self.should_trace = code_filter
        self.max_typed_dict_size = max_typed_dict_size

    def _get_func(self, frame: FrameType) -> Optional[Callable[..., Any]]:
        pass

    def handle_call(self, frame: FrameType) -> None:
        pass

    def handle_return(self, frame: FrameType, arg: Any) -> None:
        # In the case of a 'return' event, arg contains the return value, or
        # None, if the block returned because of an unhandled exception. We
        # need to distinguish the exceptional case (not a valid return type)
        # from a function returning (or yielding) None. In the latter case, the
        # the last instruction that was executed should always be a return or a
        # yield.
        pass

    def __call__(self, frame: FrameType, event: str, arg: Any) -> "CallTracer":
        code = frame.f_code
        if (
            event not in SUPPORTED_EVENTS
            or code.co_name == "trace_types"
            or self.should_trace
            and not self.should_trace(code)
        ):
            return self
        try:
            if event == EVENT_CALL:
                self.handle_call(frame)
            elif event == EVENT_RETURN:
                self.handle_return(frame, arg)
            else:
                logger.error("Cannot handle event %s", event)
        except Exception:
            logger.exception("Failed collecting trace")
        return self


@contextmanager
def trace_calls(
    logger: CallTraceLogger,
    max_typed_dict_size: int,
    code_filter: Optional[CodeFilter] = None,
    sample_rate: Optional[int] = None,
) -> Iterator[None]:
    """Enable call tracing for a block of code"""
    pass
