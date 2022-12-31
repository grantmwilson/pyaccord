from __future__ import annotations

from enum import IntEnum
from typing import Iterable


class Permissions(IntEnum):

    ADMINISTRATOR = 1 << 3

    @staticmethod
    def merge(permissions: Iterable[Permissions]) -> int:
        """Merges a list of permissions into a single int."""

        all_perms = 0

        for p in permissions:
            all_perms |= p

        return all_perms

    @staticmethod
    def merge_to_str(permissions: Iterable[Permissions]) -> str:

        return str(Permissions.merge(permissions))
