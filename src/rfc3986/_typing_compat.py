import sys
import typing as t

__all__ = ("Self",)

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
elif t.TYPE_CHECKING:
    from typing_extensions import Self
else:  # pragma: no cover

    class _PlaceholderMeta(type):
        # This is meant to make it easier to debug the presence of placeholder
        # classes.
        def __repr__(self):
            return f"placeholder for typing.{self.__name__}"

    class Self(metaclass=_PlaceholderMeta):
        """Placeholder for "typing.Self"."""
