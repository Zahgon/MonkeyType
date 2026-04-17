# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import argparse
import collections
import difflib
import importlib
import inspect
import os
import os.path
import runpy
import sys
from pathlib import Path
from typing import IO, TYPE_CHECKING, List, Optional, Tuple

from libcst import Module, parse_module
from libcst.codemod import CodemodContext
from libcst.codemod.visitors import (
    ApplyTypeAnnotationsVisitor,
    GatherImportsVisitor,
    ImportItem,
)

from monkeytype import trace
from monkeytype.config import Config
from monkeytype.exceptions import MonkeyTypeError
from monkeytype.stubs import (
    ExistingAnnotationStrategy,
    Stub,
    build_module_stubs_from_traces,
)
from monkeytype.tracing import CallTrace
from monkeytype.type_checking_imports_transformer import (
    MoveImportsToTypeCheckingBlockVisitor,
)
from monkeytype.typing import NoOpRewriter
from monkeytype.util import get_name_in_module

if TYPE_CHECKING:
    # This is not present in Python 3.6.1, so not safe for runtime import
    from typing import NoReturn  # noqa


def module_path(path: str) -> Tuple[str, Optional[str]]:
    """Parse <module>[:<qualname>] into its constituent parts."""
    pass


def module_path_with_qualname(path: str) -> Tuple[str, str]:
    """Require that path be of the form <module>:<qualname>."""
    pass


def complain_about_no_traces(args: argparse.Namespace, stderr: IO[str]) -> None:
    pass


def get_monkeytype_config(path: str) -> Config:
    """Imports the config instance specified by path.

    Path should be in the form module:qualname. Optionally, path may end with (),
    in which case we will call/instantiate the given class/function.
    """
    pass


def display_sample_count(traces: List[CallTrace], stderr: IO[str]) -> None:
    """Print to stderr the number of traces each stub is based on."""
    pass


def get_stub(
    args: argparse.Namespace, stdout: IO[str], stderr: IO[str]
) -> Optional[Stub]:
    pass


class HandlerError(Exception):
    pass


def get_newly_imported_items(
    stub_module: Module, source_module: Module
) -> List[ImportItem]:
    pass


def apply_stub_using_libcst(
    stub: str,
    source: str,
    overwrite_existing_annotations: bool,
    confine_new_imports_in_type_checking_block: bool = False,
) -> str:
    pass


def apply_stub_handler(
    args: argparse.Namespace, stdout: IO[str], stderr: IO[str]
) -> None:
    pass


def get_diff(
    args: argparse.Namespace, stdout: IO[str], stderr: IO[str]
) -> Optional[str]:
    pass


def print_stub_handler(
    args: argparse.Namespace, stdout: IO[str], stderr: IO[str]
) -> None:
    pass


def list_modules_handler(
    args: argparse.Namespace, stdout: IO[str], stderr: IO[str]
) -> None:
    pass


def run_handler(args: argparse.Namespace, stdout: IO[str], stderr: IO[str]) -> None:
    # remove initial `monkeytype run`
    pass


def update_args_from_config(args: argparse.Namespace) -> None:
    """Pull values from config for unspecified arguments."""
    pass


def main(argv: List[str], stdout: IO[str], stderr: IO[str]) -> int:
    pass


def entry_point_main() -> "NoReturn":
    """Wrapper for main() for setuptools console_script entry point."""
    # Since monkeytype needs to import the user's code (and possibly config
    # code), the user's code must be on the Python path. But when running the
    # CLI script, it won't be. So we add the current working directory to the
    # Python path ourselves.
    sys.path.insert(0, os.getcwd())
    sys.exit(main(sys.argv[1:], sys.stdout, sys.stderr))
