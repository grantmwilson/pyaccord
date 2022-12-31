
from __future__ import annotations
from enum import IntEnum

from typing import Dict, List, Optional, TYPE_CHECKING
from .exceptions import NoPyaccordClientProvidedError

from .invite import Invite

if TYPE_CHECKING:
    from client import Client


class ChannelType(IntEnum):

    GUILD_TEXT = 0


class BaseChannel:

    id: int
    type_int: int
    guild_id: Optional[int]
    position: Optional[int]
    # permission_overwrites
    raw_permission_overwrites: Optional[List[dict]]
    name: Optional[str]

    _client: Optional[Client]

    def __init__(
            self, id: int, *, type_int: int, position: Optional[int] = None, name: Optional[str],
            client: Optional[Client] = None, guild_id: Optional[int],
            raw_permission_overwrites: Optional[List[dict]] = None) -> None:

        self.id = id
        self.type_int = type_int
        self.position = position
        self.name = name
        self.guild_id = guild_id
        self.raw_permission_overwrites = raw_permission_overwrites

        self._client = client

    def __repr__(self) -> str:
        return f"<BaseChannel: {self.name} #{self.id}>"

    @staticmethod
    def from_list_of_dict(lst: List[dict], *, client: Optional[Client] = None, **kwargs) -> List[Channel]:
        channels = []
        for c in lst:
            channels.append(Channel.from_dict(c, client=client, **kwargs))

        return channels

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[Client] = None, **kwargs) -> Channel:
        return Channel(
            id=d["id"],
            guild_id=d["guild_id"],
            name=d["name"],
            type_int=d["type"],
            position=d["position"],
            raw_permission_overwrites=d["permission_overwrites"],
            client=client,
            **kwargs
        )


class Channel(BaseChannel):

    def __new__(cls, *args, type_int: int, **kwargs):
        if type_int == 0:
            return TextChannel(*args, **kwargs)

        return super(Channel, cls).__new__(cls)

    def __repr__(self) -> str:
        return f"<Channel: {self.name} #{self.id}>"


class TextChannel(BaseChannel):

    def __init__(
            self, id: int, *, position: Optional[int] = None, name: Optional[str],
            client: Optional[Client] = None, guild_id: Optional[int], **kwargs) -> None:
        super().__init__(id, position=position, name=name, client=client, guild_id=guild_id, type_int=0, **kwargs)

    def __repr__(self) -> str:
        return f"<TextChannel: {self.name} #{self.id}>"

    def create_invite(self, *, max_age: Optional[int] = None, max_uses: Optional[int] = None,
                      temporary: Optional[bool] = None, unique: Optional[bool] = None) -> Invite:

        if not self._client:
            raise NoPyaccordClientProvidedError

        return self._client.create_channel_invite(
            self, max_age=max_age, max_uses=max_uses, temporary=temporary, unique=unique)
