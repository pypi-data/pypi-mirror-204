"""The optional object implementation.

This module has the implementations for the **Optional** object.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Generic, TypeVar, Union, final

from .exceptions import ValueNotProvidedError

_T = TypeVar("_T")
_TR = TypeVar("_TR")


class Optional(ABC, Generic[_T]):
    """An optional value wrapper.

    An **Optional** object is never constructed directly. Insthead, there are methods to
    build them.

    See the [of][optional.Optional.of] and
    [empty][optional.Optional.empty] methods.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def value(self) -> _T:  # pragma: nocover
        """Get the wrapped value.

        Raises:
            ValueNotProvidedError: If the value were not provided

        Returns:
            _T: The wrapped value
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def has_value(self) -> bool:  # pragma: nocover
        """Get wether this object has a value in it.

        If the value is not present, an exception is raised.

        Returns:
            True: If the value is present
            False: If the **Optional** object is empty
        """
        raise NotImplementedError()

    @final
    @property
    def is_empty(self) -> bool:
        """Get wether this instance is empty

        This just returns the opposite of
        [has_value][optional.optional.Optional.has_value].

        Returns:
            bool: `True` if the value is not present, `False` otherwise
        """
        return not self.has_value

    @final
    def or_else(self, value: _T) -> Optional[_T]:
        """Return an optional value wrapping this.

        If this optional has a value, the value is returned. Otherwise, the supplied
        value is returned from the returned object's value property.

        Args:
            value: The value to retrieve if the instance is empty

        Returns:
            The [Optional][optional.optional.Optional] object wrapping this
        """

        return _Default(value, self)

    @final
    def map(self, mapper: Callable[[_T], _TR]) -> Optional[_TR]:
        """Build a value mapper.

        The returned value is another [Optional][optional.Optional] implementation
        that runs the _mapper_ function.

        The provided callable is run once for every instance and after the value has
        been mapped it is cached on the object.

        For example:

        ```pycon
        >>> from optional import Optional
        >>> opt=Optional.of(33).map(lambda x: x*2)
        >>> opt.value
        66
        >>>
        ```

        Args:
            mapper: The mapper function

        Returns:
            A new [Optional][optional.Optional] object
        """
        return _Mapped(self, mapper)

    @final
    def apply(
        self,
        func: Callable[[_T], None],
        *,
        if_empty: Union[Callable[[], None], None] = None,
    ) -> None:
        """Call a function if the value is present.

        Args:
            func: The code to call if the value is present
            if_empty: The function to be called if the value is not present.
        """
        if self.has_value:
            func(self.value)
        elif if_empty is not None:
            if_empty()

    @final
    async def apply_async(
        self,
        func: Callable[[_T], Awaitable[None]],
        *,
        if_empty: Union[Callable[[], Awaitable[None]], None] = None,
    ) -> None:
        """Call an async function if the value is present.

        Args:
            func: The async function to call
            if_empty: The function to be called if the value is not present.
        """
        if self.has_value:
            await func(self.value)
        elif if_empty is not None:
            await if_empty()

    @staticmethod
    def of(value: _T) -> Optional[_T]:
        """Build an [Optional][optional.Optional] object.

        Args:
            value: The value to wrap

        Returns:
            The [Optional] wrapper.
        """
        return _Value(value)

    @staticmethod
    def empty() -> Optional[Any]:
        """Build an empty [Optional][optional.optional.Optional] object.

        Returns:
            An empty optional instance
        """
        return _Empty()

    def __eq__(self, __value: Any) -> bool:
        if type(__value) != type(self):
            return NotImplemented

        if self.has_value and __value.has_value:
            # Delegate comparison to value implementations itself.
            return self.value == __value.value

        # Compare the `has_value` property:
        return self.has_value == __value.has_value

    def __bool__(self) -> bool:
        return self.has_value


class _Empty(Optional[_T], Generic[_T]):
    @final
    @property
    def value(self) -> _T:
        raise ValueNotProvidedError("Value were not provided.")

    @final
    @property
    def has_value(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Optional.empty()"

    def __str__(self) -> str:
        return "empty"


class _Value(Optional[_T], Generic[_T]):
    __slots__ = ("_value",)

    def __init__(self, value: _T) -> None:
        super().__init__()
        self._value = value

    @property
    def value(self) -> _T:
        return self._value

    @property
    def has_value(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Optional[{type(self.value).__qualname__}].of({self.value!r})"

    def __str__(self) -> str:
        return str(self.value)


class _Mapped(Optional[_TR], Generic[_T, _TR]):
    __slots__ = ("_mapped", "_mapper", "_value", "_value_set")

    def __init__(self, mapped: Optional[_T], mapper: Callable[[_T], _TR]) -> None:
        self._mapper = mapper
        self._mapped = mapped
        self._value_set = False
        self._value: Any = None

    @property
    def has_value(self) -> bool:
        return self._mapped.has_value

    @property
    def value(self) -> _TR:
        if not self._value_set:
            self._value = self._mapper(self._mapped.value)
            self._value_set = True

        return self._value  # type: ignore

    def __repr__(self) -> str:
        return f"{self._mapped!r}.map({self._mapper!r})"

    def __str__(self) -> str:
        if not self.has_value:
            return str(self._mapped)

        return str(self.value)


class _Default(Optional[_T], Generic[_T]):
    def __init__(self, value: _T, mapped: Optional[_T]) -> None:
        self._value = value
        self._mapped = mapped

    @property
    def value(self) -> _T:
        if self._mapped.has_value:
            return self._mapped.value

        return self._value

    @property
    def has_value(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"{self._mapped!r}.or_else({self._value!r})"

    def __str__(self) -> str:
        return str(self.value)
