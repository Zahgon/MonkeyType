# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import Any, ForwardRef, Union, _GenericAlias  # type: ignore[attr-defined]

from mypy_extensions import _TypedDictMeta  # type: ignore[attr-defined]

try:
    from django.utils.functional import cached_property as cp

    cached_property = cp
except ImportError:
    # Django may not be installed
    cached_property = None


def is_typed_dict(typ: type) -> bool:
    """Test indirectly using _TypedDictMeta because TypedDict does not support `isinstance`."""
    pass


def is_any(typ: Any) -> bool:
    pass


def is_union(typ: Any) -> bool:
    pass


try:
    # Python 3.9
    from typing import _SpecialGenericAlias  # type: ignore[attr-defined]

    def is_generic(typ: Any) -> bool:
        pass

except ImportError:

    def is_generic(typ: Any) -> bool:
        pass


def is_generic_of(typ: Any, gen: Any) -> bool:
    pass


def qualname_of_generic(typ: Any) -> str:
    pass


def name_of_generic(typ: Any) -> str:
    pass


def is_forward_ref(typ: Any) -> bool:
    pass


def make_forward_ref(s: str) -> ForwardRef:
    pass


def repr_forward_ref() -> str:
    """For checking the test output when ForwardRef is printed."""
    pass


def __are_typed_dict_types_equal(type1: type, type2: type) -> bool:
    """Return true if the two TypedDicts are equal.
    Doing this explicitly because
    TypedDict('Foo', {'a': int}) != TypedDict('Foo', {'a': int})."""
    pass


def types_equal(typ: type, other_type: type) -> bool:
    pass


# HACK: MonkeyType monkey-patches _TypedDictMeta!
# We need this to compare TypedDicts recursively.
_TypedDictMeta.__eq__ = __are_typed_dict_types_equal
