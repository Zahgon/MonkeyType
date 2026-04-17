# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import asyncio
import collections
import enum
import inspect
import logging
import re
from abc import ABCMeta, abstractmethod
from typing import (
    Any,
    Callable,
    DefaultDict,
    Dict,
    ForwardRef,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

from monkeytype.compat import (
    cached_property,
    is_any,
    is_forward_ref,
    is_generic,
    is_union,
    make_forward_ref,
    qualname_of_generic,
)
from monkeytype.tracing import CallTrace, CallTraceLogger
from monkeytype.typing import (
    GenericTypeRewriter,
    NoneType,
    NoOpRewriter,
    TypeRewriter,
    field_annotations,
    make_generator,
    make_iterator,
    shrink_types,
)
from monkeytype.util import get_name_in_module, pascal_case

logger = logging.getLogger(__name__)


class FunctionKind(enum.Enum):
    MODULE = 0
    CLASS = 1
    INSTANCE = 2
    STATIC = 3
    # Properties are really instance methods, but this is fine for now...
    PROPERTY = 4
    DJANGO_CACHED_PROPERTY = 5

    @classmethod
    def from_callable(cls, func: Callable[..., Any]) -> "FunctionKind":
        pass


class ExistingAnnotationStrategy(enum.Enum):
    """Strategies for handling existing annotations in the source."""

    # Attempt to replicate existing source annotations in the stub. Useful for
    # generating complete-looking stubs for inspection.
    REPLICATE = 0
    # Ignore existing annotations entirely and generate a stub purely from trace
    # data. Probably won't apply cleanly, but useful for comparison purposes.
    IGNORE = 1
    # Generate a stub that omits annotations anywhere the existing source has
    # them. Maximizes likelihood that the stub will cleanly apply using retype.
    OMIT = 2


class ImportMap(DefaultDict[Any, Any]):
    """A mapping of module name to the set of names to be imported."""

    def __init__(self) -> None:
        super().__init__(set)

    def merge(self, other: "ImportMap") -> None:
        pass


def _get_import_for_qualname(qualname: str) -> str:
    # Nested classes are annotated using the path from the root class
    # (e.g. Parent.Child, where Child is defined inside Parent)
    pass


def get_imports_for_annotation(anno: Any) -> ImportMap:
    """Return the imports (module, name) needed for the type in the annotation"""
    pass


def get_imports_for_signature(sig: inspect.Signature) -> ImportMap:
    """Return the imports (module, name) needed for all types in annotations"""
    pass


def update_signature_args(
    sig: inspect.Signature,
    arg_types: Dict[str, type],
    has_self: bool,
    existing_annotation_strategy: ExistingAnnotationStrategy = ExistingAnnotationStrategy.REPLICATE,
) -> inspect.Signature:
    """Update argument annotations with the supplied types"""
    pass


def update_signature_return(
    sig: inspect.Signature,
    return_type: Optional[type] = None,
    yield_type: Optional[type] = None,
    existing_annotation_strategy: ExistingAnnotationStrategy = ExistingAnnotationStrategy.REPLICATE,
) -> inspect.Signature:
    """Update return annotation with the supplied types"""
    pass


def shrink_traced_types(
    traces: Iterable[CallTrace],
    max_typed_dict_size: int,
) -> Tuple[Dict[str, type], Optional[type], Optional[type]]:
    """Merges the traced types and returns the minimally equivalent types"""
    pass


def get_typed_dict_class_name(parameter_name: str) -> str:
    """Return the name for a TypedDict class generated for parameter `parameter_name`."""
    pass


class Stub(metaclass=ABCMeta):
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    @abstractmethod
    def render(self) -> str:
        pass


class ImportBlockStub(Stub):
    def __init__(self, imports: Optional[ImportMap] = None) -> None:
        self.imports = imports if imports else ImportMap()

    def render(self) -> str:
        pass

    def __repr__(self) -> str:
        return "ImportBlockStub(%s)" % (repr(self.imports),)


def _is_optional(anno: Any) -> bool:
    """Is the supplied annotation an instance of the 'virtual' Optional type?

    Optional isn't really a type. It's an alias to Union[T, NoneType]
    """
    pass


def _get_optional_elem(anno: Any) -> Any:
    """Get the non-null type from an optional."""
    pass


class RenderAnnotation(GenericTypeRewriter[str]):
    """Render annotation recursively."""

    def make_anonymous_typed_dict(
        self, required_fields: Dict[str, str], optional_fields: Dict[str, str]
    ) -> str:
        pass

    def make_builtin_typed_dict(
        self, name: str, annotations: Dict[str, str], total: bool
    ) -> str:
        pass

    def generic_rewrite(self, typ: Any) -> str:
        pass

    def rewrite_container_type(self, container_type: Any) -> str:
        pass

    def rewrite_malformed_container(self, container: Any) -> str:
        pass

    def rewrite_type_variable(self, type_variable: Any) -> str:
        pass

    def make_builtin_tuple(self, elements: Iterable[str]) -> str:
        pass

    def make_container_type(self, container_type: str, elements: str) -> str:
        pass

    def rewrite_Union(self, union: type) -> str:
        pass

    def rewrite(self, typ: type) -> str:
        pass


def render_annotation(anno: Any) -> str:
    """Convert an annotation into its stub representation."""
    pass


def render_parameter(param: inspect.Parameter) -> str:
    """Convert a parameter into its stub representation.

    NB: This is copied almost entirely from https://github.com/python/cpython/blob/3.6/Lib/inspect.py
    with the modification that it calls our own rendering functions for annotations.

    TODO: push a patch upstream so we don't have to do this on Python 3.x.
    """
    pass


def render_signature(
    sig: inspect.Signature, max_line_len: Optional[int] = None, prefix: str = ""
) -> str:
    """Convert a signature into its stub representation.

    NB: This is copied almost entirely from https://github.com/python/cpython/blob/3.6/Lib/inspect.py
    with the modification that it calls our own rendering functions for annotations.

    TODO: push a patch upstream so we don't have to do this on Python 3.x.
    """
    pass


class AttributeStub(Stub):
    def __init__(
        self,
        name: str,
        typ: type,
    ) -> None:
        self.name = name
        self.typ = typ

    def render(self, prefix: str = "") -> str:
        pass

    def __repr__(self) -> str:
        return f"AttributeStub({self.name}, {self.typ})"


class FunctionStub(Stub):
    def __init__(
        self,
        name: str,
        signature: inspect.Signature,
        kind: FunctionKind,
        strip_modules: Optional[Iterable[str]] = None,
        is_async: bool = False,
    ) -> None:
        self.name = name
        self.signature = signature
        self.kind = kind
        self.strip_modules = strip_modules or []
        self.is_async = is_async

    def render(self, prefix: str = "") -> str:
        pass

    def __repr__(self) -> str:
        return "FunctionStub(%s, %s, %s, %s, %s)" % (
            repr(self.name),
            repr(self.signature),
            repr(self.kind),
            repr(self.strip_modules),
            self.is_async,
        )


class ClassStub(Stub):
    def __init__(
        self,
        name: str,
        function_stubs: Optional[Iterable[FunctionStub]] = None,
        attribute_stubs: Optional[Iterable[AttributeStub]] = None,
    ) -> None:
        self.name = name
        self.function_stubs: Dict[str, FunctionStub] = {}
        self.attribute_stubs = attribute_stubs or []
        if function_stubs is not None:
            self.function_stubs = {stub.name: stub for stub in function_stubs}

    def render(self) -> str:
        pass

    def __repr__(self) -> str:
        return "ClassStub(%s, %s, %s)" % (
            repr(self.name),
            tuple(self.function_stubs.values()),
            tuple(self.attribute_stubs),
        )


class ReplaceTypedDictsWithStubs(TypeRewriter):
    """Replace TypedDicts in a generic type with class stubs and store all the stubs."""

    def __init__(self, class_name_hint: str) -> None:
        self._class_name_hint = class_name_hint
        self.stubs: List[ClassStub] = []

    def _rewrite_container(self, cls: type, container: type) -> type:
        """Rewrite while using the index of the inner type as a class name hint.

        Otherwise, Tuple[TypedDict(...), TypedDict(...)] would give the same
        name for both the generated classes."""
        pass

    def _add_typed_dict_class_stub(
        self,
        fields: Dict[str, type],
        class_name: str,
        base_class_name: str = "TypedDict",
        total: bool = True,
    ) -> None:
        pass

    def rewrite_anonymous_TypedDict(self, typed_dict: type) -> ForwardRef:  # type: ignore[override]
        pass

    @staticmethod
    def rewrite_and_get_stubs(
        typ: type, class_name_hint: str
    ) -> Tuple[type, List[ClassStub]]:
        pass


class ModuleStub(Stub):
    def __init__(
        self,
        function_stubs: Optional[Iterable[FunctionStub]] = None,
        class_stubs: Optional[Iterable[ClassStub]] = None,
        imports_stub: Optional[ImportBlockStub] = None,
        typed_dict_class_stubs: Optional[Iterable[ClassStub]] = None,
    ) -> None:
        self.function_stubs: Dict[str, FunctionStub] = {}
        if function_stubs is not None:
            self.function_stubs = {stub.name: stub for stub in function_stubs}
        self.class_stubs: Dict[str, ClassStub] = {}
        if class_stubs is not None:
            self.class_stubs = {stub.name: stub for stub in class_stubs}
        self.imports_stub = imports_stub if imports_stub else ImportBlockStub()
        self.typed_dict_class_stubs: List[ClassStub] = []
        if typed_dict_class_stubs is not None:
            self.typed_dict_class_stubs = list(typed_dict_class_stubs)

    def render(self) -> str:
        pass

    def __repr__(self) -> str:
        return "ModuleStub(%s, %s, %s, %s)" % (
            tuple(self.function_stubs.values()),
            tuple(self.class_stubs.values()),
            repr(self.imports_stub),
            tuple(self.typed_dict_class_stubs),
        )


class FunctionDefinition:
    _KIND_WITH_SELF = {
        FunctionKind.CLASS,
        FunctionKind.INSTANCE,
        FunctionKind.PROPERTY,
        FunctionKind.DJANGO_CACHED_PROPERTY,
    }

    def __init__(
        self,
        module: str,
        qualname: str,
        kind: FunctionKind,
        sig: inspect.Signature,
        is_async: bool = False,
        typed_dict_class_stubs: Optional[Iterable[ClassStub]] = None,
    ) -> None:
        self.module = module
        self.qualname = qualname
        self.kind = kind
        self.signature = sig
        self.is_async = is_async
        self.typed_dict_class_stubs = typed_dict_class_stubs or []

    @classmethod
    def from_callable(
        cls, func: Callable[..., Any], kind: Optional[FunctionKind] = None
    ) -> "FunctionDefinition":
        pass

    @classmethod
    def from_callable_and_traced_types(
        cls,
        func: Callable[..., Any],
        arg_types: Dict[str, type],
        return_type: Optional[type],
        yield_type: Optional[type],
        existing_annotation_strategy: ExistingAnnotationStrategy = ExistingAnnotationStrategy.REPLICATE,
    ) -> "FunctionDefinition":
        pass

    @property
    def has_self(self) -> bool:
        pass

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self) -> str:
        return "FunctionDefinition('%s', '%s', %s, %s, %s, %s)" % (
            self.module,
            self.qualname,
            self.kind,
            self.signature,
            self.is_async,
            self.typed_dict_class_stubs,
        )


def get_updated_definition(
    func: Callable[..., Any],
    traces: Iterable[CallTrace],
    max_typed_dict_size: int,
    rewriter: Optional[TypeRewriter] = None,
    existing_annotation_strategy: ExistingAnnotationStrategy = ExistingAnnotationStrategy.REPLICATE,
) -> FunctionDefinition:
    """Update the definition for func using the types collected in traces."""
    pass


def build_module_stubs(entries: Iterable[FunctionDefinition]) -> Dict[str, ModuleStub]:
    """Given an iterable of function definitions, build the corresponding stubs"""
    pass


def build_module_stubs_from_traces(
    traces: Iterable[CallTrace],
    max_typed_dict_size: int,
    existing_annotation_strategy: ExistingAnnotationStrategy = ExistingAnnotationStrategy.REPLICATE,
    rewriter: Optional[TypeRewriter] = None,
) -> Dict[str, ModuleStub]:
    """Given an iterable of call traces, build the corresponding stubs."""
    pass


class StubIndexBuilder(CallTraceLogger):
    """Builds type stub index directly from collected call traces."""

    def __init__(self, module_re: str, max_typed_dict_size: int) -> None:
        self.re = re.compile(module_re)
        self.index: DefaultDict[Callable[..., Any], Set[CallTrace]] = (
            collections.defaultdict(set)
        )
        self.max_typed_dict_size = max_typed_dict_size

    def log(self, trace: CallTrace) -> None:
        pass

    def get_stubs(self) -> Dict[str, ModuleStub]:
        pass
