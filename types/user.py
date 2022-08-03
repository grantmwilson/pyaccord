from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pyaccord.DiscordAPIClient import DiscordAPIClient
    from pyaccord.types.guild import Guild


class User:

    id: int
    username: Optional[str]
    discriminator: Optional[str]
    _client: Optional[DiscordAPIClient]
    _is_current_user: bool

    def __init__(
            self, id: int, username: Optional[str] = None, discriminator: Optional[str] = None, *,
            client: Optional[DiscordAPIClient] = None) -> None:
        self.id = id
        self.username = username
        self.discriminator = discriminator
        self._client = client

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[DiscordAPIClient] = None, **kwargs) -> User:
        return User(
            id=d["id"],
            username=d["username"],
            discriminator=d["discriminator"],
            client=client,
            **kwargs
        )

    def __repr__(self) -> str:
        return f"<User: {self.username}#{self.discriminator} with id: {self.id}>"


class CurrentUser(User):

    @property
    def guilds(self) -> List[Guild]:
        """Gets the user guilds, only for the current user."""
        if self._client:
            return self._client.get_current_user_guilds()
        else:
            raise Exception("No Pyaccord client provided.")

    def __repr__(self) -> str:
        return f"<CurrentUser: {self.username}#{self.discriminator} with id: {self.id}>"

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[DiscordAPIClient] = None, **kwargs) -> CurrentUser:
        return CurrentUser(
            id=d["id"],
            username=d["username"],
            discriminator=d["discriminator"],
            client=client,
            **kwargs
        )
