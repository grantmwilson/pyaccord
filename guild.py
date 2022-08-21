from __future__ import annotations

from typing import Dict, List, Optional, TYPE_CHECKING
from .channel import Channel
from .role import Role
from .exceptions import NoPyaccordClientProvidedError


if TYPE_CHECKING:
    from client import Client


class Guild:

    id: int
    name: str
    _roles: Optional[List[Role]]
    _channels: Optional[List[Channel]]
    _public_updates_channel_id: Optional[int]

    _client: Optional[Client]

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[Client] = None, **kwargs) -> Guild:

        # print(d)

        guild = Guild(
            id=d["id"],
            name=d["name"],
            client=client,
            **kwargs
        )

        guild._roles = Role.from_list_of_dict(d["roles"], client=client) if "roles" in d else None
        guild._public_updates_channel_id = d["public_updates_channel_id"] if "public_updates_channel_id" in d else None

        return guild

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

    def create_role(self,
                    name: Optional[str] = None, *,
                    permissions: Optional[int] = None,
                    color: Optional[int] = None,
                    hoist: Optional[bool] = False,
                    mentionable: Optional[bool] = False) -> Role:

        if not self._client:
            raise NoPyaccordClientProvidedError

        new_role = self._client.create_guild_role(
            self.id, name=name, permissions=permissions, color=color, hoist=hoist, mentionable=mentionable)

        return new_role

    @property
    def roles(self) -> List[Role]:
        if not self._roles:
            return self.get_roles()

        return self._roles

    def get_roles(self) -> List[Role]:
        """Gets the guild's roles from the server and updates the roles list."""

        if not self._client:
            raise NoPyaccordClientProvidedError

        self._roles = self._client.get_guild_roles(self)

        return self._roles

    @property
    def channels(self) -> List[Channel]:
        if not hasattr(self, "_channels") or not self._channels:
            return self.get_channels()

        return self._channels

    def get_channels(self) -> List[Channel]:

        if not self._client:
            raise NoPyaccordClientProvidedError

        self._channels = self._client.get_guild_channels(self)

        return self._channels
