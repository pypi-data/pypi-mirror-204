from collections.abc import Iterable
from typing import Final, Literal, Protocol, TypeAlias, TypedDict, Union

__all__: Final[tuple[str, ...]] = (
    "ASGIReceiveCallable",
    "ASGIReceiveEvent",
    "ASGISendCallable",
    "ASGISendEvent",
    "ASGIVersions",
    "HTTPConnectionScope",
    "HTTPDisconnectEvent",
    "HTTPRequestEvent",
    "HTTPResponseBodyEvent",
    "HTTPResponseStartEvent",
    "LifespanScope",
    "LifespanShutdownCompleteEvent",
    "LifespanShutdownEvent",
    "LifespanShutdownFailedEvent",
    "LifespanStartupCompleteEvent",
    "LifespanStartupEvent",
    "LifespanStartupFailedEvent",
    "Scope",
)


class ASGIVersions(TypedDict, total=False):
    spec_version: str
    version: str


class HTTPConnectionScope(TypedDict, total=False):
    type: Literal["http"]
    asgi: ASGIVersions
    http_version: str
    method: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[tuple[bytes, bytes]]
    client: tuple[str, int] | None
    server: tuple[str, int | None] | None


class HTTPRequestEvent(TypedDict):
    type: Literal["http.request"]
    body: bytes
    more_body: bool


class HTTPResponseStartEvent(TypedDict, total=False):
    type: Literal["http.response.start"]
    status: int
    headers: Iterable[tuple[bytes, bytes]]


class HTTPResponseBodyEvent(TypedDict):
    type: Literal["http.response.body"]
    body: bytes
    more_body: bool


class HTTPDisconnectEvent(TypedDict):
    type: Literal["http.disconnect"]


class LifespanScope(TypedDict, total=False):
    type: Literal["lifespan"]
    asgi: ASGIVersions


class LifespanStartupEvent(TypedDict):
    type: Literal["lifespan.startup"]


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal["lifespan.startup.complete"]


class LifespanStartupFailedEvent(TypedDict):
    type: Literal["lifespan.startup.failed"]
    message: str


class LifespanShutdownEvent(TypedDict):
    type: Literal["lifespan.shutdown"]


class LifespanShutdownCompleteEvent(TypedDict):
    type: Literal["lifespan.shutdown.complete"]


class LifespanShutdownFailedEvent(TypedDict):
    type: Literal["lifespan.shutdown.failed"]
    message: str


Scope: TypeAlias = Union[
    HTTPConnectionScope,
    LifespanScope,
]
ASGIReceiveEvent: TypeAlias = Union[
    HTTPRequestEvent,
    HTTPDisconnectEvent,
    LifespanStartupEvent,
    LifespanShutdownEvent,
]
ASGISendEvent: TypeAlias = Union[
    HTTPResponseStartEvent,
    HTTPResponseBodyEvent,
    HTTPDisconnectEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
]


class ASGIReceiveCallable(Protocol):
    async def __call__(self) -> ASGIReceiveEvent:
        ...


class ASGISendCallable(Protocol):
    async def __call__(self, event: ASGISendEvent) -> None:
        ...
