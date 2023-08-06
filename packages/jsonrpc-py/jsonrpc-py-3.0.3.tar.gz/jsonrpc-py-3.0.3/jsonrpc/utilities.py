from asyncio import AbstractEventLoop, Future, get_running_loop
from collections.abc import Callable, Iterable, MutableMapping
from contextvars import Context, copy_context
from functools import partial
from inspect import iscoroutinefunction
from typing import Any, Final, Literal, ParamSpec, TypeGuard, final

__all__: Final[tuple[str, ...]] = (
    "ensure_async",
    "is_iterable",
    "make_hashable",
    "Undefined",
    "UndefinedType",
)

P = ParamSpec("P")


def ensure_async(user_function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs) -> Future[Any]:
    loop: AbstractEventLoop = get_running_loop()
    context: Context = copy_context()

    if iscoroutinefunction(callback := partial(user_function, *args, **kwargs)):
        return loop.create_task(callback(), context=context)
    else:
        return loop.run_in_executor(None, context.run, callback)


def is_iterable(obj: Any, /) -> TypeGuard[Iterable[Any]]:
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def make_hashable(obj: Any, /) -> Any:
    if isinstance(obj, MutableMapping):
        return tuple((key, make_hashable(value)) for key, value in sorted(obj.items()))
    #: ---
    #: Try hash to avoid converting a hashable iterable (e.g. string, frozenset)
    #: to a tuple:
    try:
        hash(obj)
    except TypeError:
        if is_iterable(obj):
            return tuple(map(make_hashable, obj))
        #: ---
        #: Non-hashable, non-iterable:
        raise

    return obj


@final
class UndefinedType:
    __slots__: tuple[str, ...] = ()

    def __repr__(self) -> Literal["Undefined"]:
        return "Undefined"

    def __hash__(self) -> Literal[0xBAADF00D]:
        return 0xBAADF00D

    def __eq__(self, obj: Any) -> bool:
        return isinstance(obj, self.__class__)

    def __bool__(self) -> Literal[False]:
        return False


Undefined: Final[UndefinedType] = UndefinedType()
