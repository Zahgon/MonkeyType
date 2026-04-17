# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import importlib
import inspect
import re
import types
from typing import Any, Callable, Optional

from monkeytype.compat import cached_property
from monkeytype.exceptions import InvalidTypeError, NameLookupError


def get_func_fqname(func: Callable[..., Any]) -> str:
    """Return the fully qualified function name."""
    pass


def get_func_in_module(module: str, qualname: str) -> Callable[..., Any]:
    """Return the function specified by qualname in module.

    Raises:
        NameLookupError if we can't find the named function
        InvalidTypeError if we the name isn't a function
    """
    pass


def get_name_in_module(
    module: str,
    qualname: str,
    attr_getter: Optional[Callable[[Any, str], Any]] = None,
) -> Any:
    """Return the python object specified by qualname in module.

    Raises:
        NameLookupError if the module/qualname cannot be retrieved.
    """
    pass


def pascal_case(s: str) -> str:
    pass
