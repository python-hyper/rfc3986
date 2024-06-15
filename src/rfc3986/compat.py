# Copyright (c) 2014 Rackspace
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Compatibility module for Python 2 and 3 support."""
import typing as t

__all__ = (
    "to_bytes",
    "to_str",
)


@t.overload
def to_str(b: t.Union[str, bytes], encoding: str = "utf-8") -> str:
    ...


@t.overload
def to_str(b: None, encoding: str = "utf-8") -> None:
    ...


def to_str(
    b: t.Optional[t.Union[str, bytes]],
    encoding: str = "utf-8",
) -> t.Optional[str]:
    """Ensure that b is text in the specified encoding."""
    if hasattr(b, "decode") and not isinstance(b, str):
        b = b.decode(encoding)
    return b


@t.overload
def to_bytes(s: t.Union[str, bytes], encoding: str = "utf-8") -> bytes:
    ...


@t.overload
def to_bytes(s: None, encoding: str = "utf-8") -> None:
    ...


def to_bytes(
    s: t.Optional[t.Union[str, bytes]],
    encoding: str = "utf-8",
) -> t.Optional[bytes]:
    """Ensure that s is converted to bytes from the encoding."""
    if hasattr(s, "encode") and not isinstance(s, bytes):
        s = s.encode(encoding)
    return s
