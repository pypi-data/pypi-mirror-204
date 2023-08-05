use once_cell::sync::Lazy;
use rustc_hash::{FxHashMap, FxHashSet};

// See: https://pypi.org/project/typing-extensions/
pub static TYPING_EXTENSIONS: Lazy<FxHashSet<&'static str>> = Lazy::new(|| {
    FxHashSet::from_iter([
        "Annotated",
        "Any",
        "AsyncContextManager",
        "AsyncGenerator",
        "AsyncIterable",
        "AsyncIterator",
        "Awaitable",
        "ChainMap",
        "ClassVar",
        "Concatenate",
        "ContextManager",
        "Coroutine",
        "Counter",
        "DefaultDict",
        "Deque",
        "Final",
        "Literal",
        "LiteralString",
        "NamedTuple",
        "Never",
        "NewType",
        "NotRequired",
        "OrderedDict",
        "ParamSpec",
        "ParamSpecArgs",
        "ParamSpecKwargs",
        "Protocol",
        "Required",
        "Self",
        "TYPE_CHECKING",
        "Text",
        "Type",
        "TypeAlias",
        "TypeGuard",
        "TypeVar",
        "TypeVarTuple",
        "TypedDict",
        "Unpack",
        "assert_never",
        "assert_type",
        "clear_overloads",
        "final",
        "get_type_hints",
        "get_args",
        "get_origin",
        "get_overloads",
        "is_typeddict",
        "overload",
        "override",
        "reveal_type",
        "runtime_checkable",
    ])
});

// See: https://docs.python.org/3/library/typing.html
pub const SUBSCRIPTS: &[&[&str]] = &[
    // builtins
    &["", "dict"],
    &["", "frozenset"],
    &["", "list"],
    &["", "set"],
    &["", "tuple"],
    &["", "type"],
    // `collections`
    &["collections", "ChainMap"],
    &["collections", "Counter"],
    &["collections", "OrderedDict"],
    &["collections", "defaultdict"],
    &["collections", "deque"],
    // `collections.abc`
    &["collections", "abc", "AsyncGenerator"],
    &["collections", "abc", "AsyncIterable"],
    &["collections", "abc", "AsyncIterator"],
    &["collections", "abc", "Awaitable"],
    &["collections", "abc", "ByteString"],
    &["collections", "abc", "Callable"],
    &["collections", "abc", "Collection"],
    &["collections", "abc", "Container"],
    &["collections", "abc", "Coroutine"],
    &["collections", "abc", "Generator"],
    &["collections", "abc", "ItemsView"],
    &["collections", "abc", "Iterable"],
    &["collections", "abc", "Iterator"],
    &["collections", "abc", "KeysView"],
    &["collections", "abc", "Mapping"],
    &["collections", "abc", "MappingView"],
    &["collections", "abc", "MutableMapping"],
    &["collections", "abc", "MutableSequence"],
    &["collections", "abc", "MutableSet"],
    &["collections", "abc", "Reversible"],
    &["collections", "abc", "Sequence"],
    &["collections", "abc", "Set"],
    &["collections", "abc", "ValuesView"],
    // `contextlib`
    &["contextlib", "AbstractAsyncContextManager"],
    &["contextlib", "AbstractContextManager"],
    // `re`
    &["re", "Match"],
    &["re", "Pattern"],
    // `typing`
    &["typing", "AbstractSet"],
    &["typing", "AsyncContextManager"],
    &["typing", "AsyncGenerator"],
    &["typing", "AsyncIterator"],
    &["typing", "Awaitable"],
    &["typing", "BinaryIO"],
    &["typing", "ByteString"],
    &["typing", "Callable"],
    &["typing", "ChainMap"],
    &["typing", "ClassVar"],
    &["typing", "Collection"],
    &["typing", "Concatenate"],
    &["typing", "Container"],
    &["typing", "ContextManager"],
    &["typing", "Coroutine"],
    &["typing", "Counter"],
    &["typing", "DefaultDict"],
    &["typing", "Deque"],
    &["typing", "Dict"],
    &["typing", "Final"],
    &["typing", "FrozenSet"],
    &["typing", "Generator"],
    &["typing", "Generic"],
    &["typing", "IO"],
    &["typing", "ItemsView"],
    &["typing", "Iterable"],
    &["typing", "Iterator"],
    &["typing", "KeysView"],
    &["typing", "List"],
    &["typing", "Mapping"],
    &["typing", "Match"],
    &["typing", "MutableMapping"],
    &["typing", "MutableSequence"],
    &["typing", "MutableSet"],
    &["typing", "Optional"],
    &["typing", "OrderedDict"],
    &["typing", "Pattern"],
    &["typing", "Reversible"],
    &["typing", "Sequence"],
    &["typing", "Set"],
    &["typing", "TextIO"],
    &["typing", "Tuple"],
    &["typing", "Type"],
    &["typing", "TypeGuard"],
    &["typing", "Union"],
    &["typing", "Unpack"],
    &["typing", "ValuesView"],
    // `typing.io`
    &["typing", "io", "BinaryIO"],
    &["typing", "io", "IO"],
    &["typing", "io", "TextIO"],
    // `typing.re`
    &["typing", "re", "Match"],
    &["typing", "re", "Pattern"],
    // `typing_extensions`
    &["typing_extensions", "AsyncContextManager"],
    &["typing_extensions", "AsyncGenerator"],
    &["typing_extensions", "AsyncIterable"],
    &["typing_extensions", "AsyncIterator"],
    &["typing_extensions", "Awaitable"],
    &["typing_extensions", "ChainMap"],
    &["typing_extensions", "ClassVar"],
    &["typing_extensions", "Concatenate"],
    &["typing_extensions", "ContextManager"],
    &["typing_extensions", "Coroutine"],
    &["typing_extensions", "Counter"],
    &["typing_extensions", "DefaultDict"],
    &["typing_extensions", "Deque"],
    &["typing_extensions", "Type"],
    // `weakref`
    &["weakref", "WeakKeyDictionary"],
    &["weakref", "WeakSet"],
    &["weakref", "WeakValueDictionary"],
];

// See: https://docs.python.org/3/library/typing.html
pub const PEP_593_SUBSCRIPTS: &[&[&str]] = &[
    // `typing`
    &["typing", "Annotated"],
    // `typing_extensions`
    &["typing_extensions", "Annotated"],
];

// See: https://peps.python.org/pep-0585/
pub const PEP_585_BUILTINS_ELIGIBLE: &[&[&str]] = &[
    &["typing", "Dict"],
    &["typing", "FrozenSet"],
    &["typing", "List"],
    &["typing", "Set"],
    &["typing", "Tuple"],
    &["typing", "Type"],
    &["typing_extensions", "Type"],
];

// See: https://github.com/JelleZijlstra/autotyping/blob/0adba5ba0eee33c1de4ad9d0c79acfd737321dd9/autotyping/autotyping.py#L69-L91
pub static SIMPLE_MAGIC_RETURN_TYPES: Lazy<FxHashMap<&'static str, &'static str>> =
    Lazy::new(|| {
        FxHashMap::from_iter([
            ("__str__", "str"),
            ("__repr__", "str"),
            ("__len__", "int"),
            ("__length_hint__", "int"),
            ("__init__", "None"),
            ("__del__", "None"),
            ("__bool__", "bool"),
            ("__bytes__", "bytes"),
            ("__format__", "str"),
            ("__contains__", "bool"),
            ("__complex__", "complex"),
            ("__int__", "int"),
            ("__float__", "float"),
            ("__index__", "int"),
            ("__setattr__", "None"),
            ("__delattr__", "None"),
            ("__setitem__", "None"),
            ("__delitem__", "None"),
            ("__set__", "None"),
            ("__instancecheck__", "bool"),
            ("__subclasscheck__", "bool"),
        ])
    });
