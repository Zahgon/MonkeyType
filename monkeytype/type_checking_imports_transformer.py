# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import List, Tuple, Union, cast

import libcst
from libcst import (
    BaseCompoundStatement,
    BaseSmallStatement,
    BaseSuite,
    CSTTransformer,
    FlattenSentinel,
    Import,
    ImportFrom,
    ImportStar,
    MaybeSentinel,
    Module,
    RemovalSentinel,
    RemoveFromParent,
    SimpleStatementLine,
)
from libcst.codemod import CodemodContext, ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor, GatherImportsVisitor, ImportItem
from libcst.helpers import get_absolute_module_from_package_for_import


class MoveImportsToTypeCheckingBlockVisitor(ContextAwareTransformer):
    CONTEXT_KEY = "MoveImportsToTypeCheckingBlockVisitor"

    def __init__(
        self,
        context: CodemodContext,
    ) -> None:
        super().__init__(context)

        self.import_items_to_be_moved: List[ImportItem] = []

    @staticmethod
    def store_imports_in_context(
        context: CodemodContext,
        import_items_to_be_moved: List[ImportItem],
    ) -> None:
        pass

    @staticmethod
    def _add_type_checking_import(source_module: Module) -> Module:
        pass

    def _remove_imports(self, tree: Module) -> Module:
        pass

    def _get_import_module(self) -> Module:
        pass

    @staticmethod
    def _replace_pass_with_imports(
        placeholder_module: Module, import_module: Module
    ) -> Module:
        pass

    def _split_module(
        self, module: Module
    ) -> Tuple[
        List[Union[SimpleStatementLine, BaseCompoundStatement]],
        List[Union[SimpleStatementLine, BaseCompoundStatement]],
    ]:
        pass

    def _add_if_type_checking_block(self, module: Module) -> Module:
        pass

    @staticmethod
    def _remove_typing_module(import_item_list: List[ImportItem]) -> List[ImportItem]:
        pass

    def transform_module_impl(
        self,
        tree: Module,
    ) -> Module:
        # Add from typing import TYPE_CHECKING
        pass


class RemoveImportsTransformer(CSTTransformer):
    def __init__(
        self,
        import_items_to_be_removed: List[ImportItem],
    ) -> None:
        super().__init__()
        self.import_items_to_be_removed = import_items_to_be_removed

    def leave_Import(
        self, original_node: Import, updated_node: Import
    ) -> Union[
        BaseSmallStatement, FlattenSentinel[BaseSmallStatement], RemovalSentinel
    ]:
        pass

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[
        BaseSmallStatement, FlattenSentinel[BaseSmallStatement], RemovalSentinel
    ]:
        pass
