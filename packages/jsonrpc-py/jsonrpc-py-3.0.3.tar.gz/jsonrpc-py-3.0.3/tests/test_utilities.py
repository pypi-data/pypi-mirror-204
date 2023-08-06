from typing import Any, Literal
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock, sentinel

from jsonrpc.utilities import Undefined, UndefinedType, ensure_async, make_hashable


class TestHashable(TestCase):
    def test_equality(self) -> None:
        tests: tuple[tuple[Any, Any], ...] = (
            ([], ()),
            (["a", 1], ("a", 1)),
            ({}, ()),
            ({"a"}, ("a",)),
            (frozenset({"a"}), {"a"}),
            ({"a": 1, "b": 2}, (("a", 1), ("b", 2))),
            ({"b": 2, "a": 1}, (("a", 1), ("b", 2))),
            (("a", ["b", 1]), ("a", ("b", 1))),
            (("a", {"b": 1}), ("a", (("b", 1),))),
        )
        for actual, expected in tests:
            with self.subTest(actual=actual):
                self.assertEqual(make_hashable(actual), expected)

    def test_count_equality(self) -> None:
        tests: tuple[tuple[Any, Any], ...] = (
            ({"a": 1, "b": ["a", 1]}, (("a", 1), ("b", ("a", 1)))),
            ({"a": 1, "b": ("a", [1, 2])}, (("a", 1), ("b", ("a", (1, 2))))),
        )
        for actual, expected in tests:
            with self.subTest(actual=actual):
                self.assertCountEqual(make_hashable(actual), expected)

    def test_unhashable(self) -> None:
        class Unhashable:
            __hash__: Literal[None] = None

        with self.assertRaises(TypeError) as context:
            make_hashable(Unhashable())

        self.assertIn("unhashable type", str(context.exception))


class TestUndefined(TestCase):
    def test_hash(self) -> None:
        self.assertEqual(hash(Undefined), 0xBAADF00D)

    def test_equality(self) -> None:
        self.assertEqual(Undefined, UndefinedType())
        self.assertNotEqual(Undefined, None)

    def test_is_truth(self) -> None:
        self.assertFalse(Undefined)


class TestUtilities(IsolatedAsyncioTestCase):
    async def test_ensure_async(self) -> None:
        for mock in (
            MagicMock(return_value=sentinel.sync_def),
            AsyncMock(return_value=sentinel.async_def),
        ):
            with self.subTest(mock=mock):
                result: Any = await ensure_async(mock, 1, 2, 3, key="value")
                self.assertIs(result, mock.return_value)
                mock.assert_called_once_with(1, 2, 3, key="value")
