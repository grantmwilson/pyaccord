from __future__ import annotations

from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pyaccord.DiscordAPIClient import DiscordAPIClient


class Guild:

    id: int
    name: str
    _client: Optional[DiscordAPIClient]

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[DiscordAPIClient] = None, **kwargs) -> Guild:
        return Guild(
            id=d["id"],
            name=d["name"],
            client=client,
            **kwargs
        )

    @staticmethod
    def from_list_of_dict(l: List[Dict], *, client: Optional[DiscordAPIClient] = None, **kwargs) -> List[Guild]:
        guilds = []
        for g in l:
            guilds.append(Guild.from_dict(g, client=client, **kwargs))

        return guilds

    def __init__(self, id: int, name: str, *, client: Optional[DiscordAPIClient] = None) -> None:
        self.id = id
        self.name = name
        self._client = client

    def __repr__(self) -> str:
        return f"<Guild: {self.name} #{self.id}>"
