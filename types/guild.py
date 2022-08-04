from __future__ import annotations

from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pyaccord.client import Client


class Guild:

    id: int
    name: str
    _client: Optional[Client]

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[Client] = None, **kwargs) -> Guild:
        return Guild(
            id=d["id"],
            name=d["name"],
            client=client,
            **kwargs
        )

    @staticmethod
    def from_list_of_dict(lst: List[Dict], *, client: Optional[Client] = None, **kwargs) -> List[Guild]:
        guilds = []
        for g in lst:
            guilds.append(Guild.from_dict(g, client=client, **kwargs))

        return guilds

    def __init__(self, id: int, name: str, *, client: Optional[Client] = None) -> None:
        self.id = id
        self.name = name
        self._client = client

    def __repr__(self) -> str:
        return f"<Guild: {self.name} #{self.id}>"
