from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from client import Client


class Role:

    id: int
    name: Optional[str]
    position: Optional[int]
    hoist: Optional[bool]
    managed: Optional[bool]
    mentionable: Optional[bool]
    # color: int

    _client: Optional[Client]

    def __init__(
            self, id: int, name: Optional[str] = None, *, position: Optional[int] = None, hoist: Optional[bool] = None,
            managed: Optional[bool] = None, mentionable: Optional[bool] = None, client: Optional[Client] = None) -> None:

        self.id = id
        self.name = name
        self.position = position
        self.hoist = hoist
        self.managed = managed
        self.mentionable = mentionable

        self._client = client

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[Client] = None) -> Role:

        return Role(
            id=d["id"],
            name=d["name"],
            position=d["position"],
            hoist=d["hoist"],
            managed=d["managed"],
            mentionable=d["mentionable"],
            client=client
        )

    @staticmethod
    def from_list_of_dict(lst: List[Dict], *, client: Optional[Client] = None, **kwargs) -> List[Role]:
        roles = []
        for r in lst:
            roles.append(Role.from_dict(r, client=client, **kwargs))

        return roles

    def __str__(self) -> str:
        if self.name:
            return f"<Role: {self.name} #{self.id}>"
        return f"<Role #{self.id}>"
