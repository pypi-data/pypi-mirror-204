from json import dumps as json_dumps, loads as json_loads
from typing import Any, Final

from .errors import Error, ErrorEnum

__all__: Final[tuple[str, ...]] = ("JSONSerializer",)


class JSONSerializer:
    """
    Simple class for JSON serialization and deserialization.
    """

    __slots__: tuple[str, ...] = ()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def serialize(self, obj: Any, /) -> bytes:
        """
        Returns the JSON representation of a value.

        :param obj: An any type of object that must be JSON serializable.
        :raises jsonrpc.Error: If any exception has occurred due the serialization or/and encoding to :py:class:`bytes`.
        :returns: The :py:class:`bytes` object containing the serialized Python data structure.
        """
        try:
            return json_dumps(obj, ensure_ascii=True, separators=(",", ":")).encode("ascii")
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to serialize object to JSON") from exc

    def deserialize(self, obj: bytes, /) -> Any:
        """
        Returns the value encoded in JSON in appropriate Python type.

        :param obj: The :py:class:`bytes` object containing the serialized JSON document.
        :raises jsonrpc.Error: If any exception has occurred due the deserialization or/and decoding from :py:class:`bytes`.
        :returns: An any type of object containing the deserialized Python data structure.
        """
        try:
            return json_loads(obj)
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to deserialize object from JSON") from exc
