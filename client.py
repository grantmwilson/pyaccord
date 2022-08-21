"""API calls for performing Discord API actions."""

from __future__ import annotations

from typing import Dict, List, Optional, Union
import requests
import logging
from channel import BaseChannel, Channel

from guild import Guild
from invite import Invite
from role import Role
from user import CurrentUser
from url_functions import get_api_url

logger = logging.getLogger("DiscordAPI")


class Client:
    """Class for performing generic Discord API actions."""

    def __init__(self, bot_token: str, *, api_version: Optional[int] = None) -> None:
        """Initialize Discord API."""

        self.bot_token = bot_token
        self.api_version = api_version

        self.headers = {
            "User-Agent": "WebsiteServerClient (engfrosh.com, 1)",
            "authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }

    @property
    def api_url(self) -> str:
        return get_api_url(self.api_version)

    # region Guilds

    def create_guild(self, name: str) -> Guild:
        """
        Create a new guild.

        """

        data = {
            "name": name
        }

        url = self.api_url + "/guilds"
        r = requests.post(url, headers=self.headers, json=data)

        r.raise_for_status()

        guild = Guild.from_dict(r.json(), client=self)

        logger.info(f"Guild created: {guild}")

        return guild

    def get_guild(self, guild: int | Guild) -> Optional[Guild]:
        """Get a guild by id"""

        if isinstance(guild, Guild):
            guild_id = guild.id
        else:
            guild_id = guild

        url = self.api_url + f"/guilds/{guild_id}"
        r = requests.get(url, headers=self.headers)

        if not r.ok:
            logger.error(f"{r.content}")
        r.raise_for_status()

        json_response = r.json()

        print(json_response)

        guild = Guild.from_dict(json_response, client=self)

        logger.debug(f"Got guild: {guild}")

        return guild

    def delete_guild(self, id: int) -> None:
        """Deletes the specified guild. Bot must be the owner."""

        url = self.api_url + f"/guilds/{id}"
        r = requests.delete(url, headers=self.headers)

        r.raise_for_status()

        logger.info(f"Deleted guild with id: {id}")

    # endregion

    # region Users

    # region Current User

    @property
    def current_user(self) -> CurrentUser:
        return self.get_current_user()

    def get_current_user(self) -> CurrentUser:
        """Get the current user."""

        url = self.api_url + "/users/@me"
        r = requests.get(url, headers=self.headers)

        if not r.ok:
            logger.error(f"{r.content}")
        r.raise_for_status()

        user = CurrentUser.from_dict(r.json(), client=self)

        logger.debug(f"Got current user: {user}")

        return user

    def get_current_user_guilds(self) -> List[Guild]:
        """Gets the guild the user is in."""

        url = self.api_url + "/users/@me/guilds"
        r = requests.get(url, headers=self.headers)

        r.raise_for_status()

        guilds = Guild.from_list_of_dict(r.json(), client=self)

        logger.debug(f"Got current user guilds: {guilds}")

        return guilds

    # endregion

    # endregion

    def create_guild_role(self, guild_id: int, *,
                          name: Optional[str] = None,
                          permissions: Optional[int] = None,
                          color: Optional[int] = None,
                          hoist: Optional[bool] = False,
                          mentionable: Optional[bool] = False) -> Role:
        """
        Create a new guild role.

        Parameters
        ----------
            mentionable: whether the role can be mentioned
            hoist: whether the role should be shown separately
            permissions, the bitwise representation of permissions
            color, hex color code

        Returns: guild id
        """

        data = {}

        for title, item in [
            ("name", name),
            ("permissions", permissions),
            ("color", color),
            ("hoist", hoist),
            ("mentionable", mentionable)
        ]:
            if item is not None:
                data[title] = item

        url = get_api_url(self.api_version) + f"/guilds/{guild_id}/roles"
        response = requests.post(url, headers=self.headers, json=data)

        response.raise_for_status()

        role = Role.from_dict(response.json(), client=self)

        logger.info(f"Created new guild role {role.name} with snowflake: {role.id}")

        return role

    def get_guild_roles(self, guild: Union[Guild, int]) -> List[Role]:
        """Get a guild's roles by guild id or Guild object."""

        if isinstance(guild, Guild):
            guild_id = guild.id
        else:
            guild_id = guild

        url = self.api_url + f"/guilds/{guild_id}/roles"
        r = requests.get(url, headers=self.headers)

        if not r.ok:
            logger.error((f"{r.content}"))
        r.raise_for_status()

        roles = Role.from_list_of_dict(r.json(), client=self)

        return roles

    def get_guild_channels(self, guild: Guild | int) -> List[Channel]:
        """Get a guild's channels by guild id or Guild object."""

        if isinstance(guild, Guild):
            guild_id = guild.id
        else:
            guild_id = guild

        url = self.api_url + f"/guilds/{guild_id}/channels"
        r = requests.get(url, headers=self.headers)

        r.raise_for_status()

        channels = Channel.from_list_of_dict(r.json(), client=self)

        return channels

    def get_channel(self, channel_id: int) -> dict:
        """Get the channel information."""

        url = get_api_url(self.api_version) + f"/channels/{channel_id}"
        response = requests.get(url, headers=self.headers)

        response.raise_for_status()

        json_response = response.json()

        logger.debug(f"Got channel info: {json_response}")

        return json_response

    def get_channel_overwrites(self, channel_id: int) -> List[Dict[str, Union[str, int]]]:
        """Get all the current overwrites for a channel."""

        channel = self.get_channel(channel_id)

        return channel["permission_overwrites"]

    def modify_channel_overwrites(self, channel_id: int, overwrites: Union[dict, List[dict]]):
        """Change the permission overwrites for the given channel.

        Parameters
        ==========
            overwrites: a dictionary or a list of dictionaries representing all the overwrites.

        """

        data = {}

        if isinstance(overwrites, dict):
            overwrites["allow"] = str(overwrites["allow"])
            overwrites["deny"] = str(overwrites["deny"])
            data["permission_overwrites"] = [overwrites]
        elif isinstance(overwrites, list):
            for i in range(len(overwrites)):
                overwrites[i]["allow"] = str(overwrites[i]["allow"])
                overwrites[i]["deny"] = str(overwrites[i]["deny"])
            data["permission_overwrites"] = overwrites

        url = get_api_url(self.api_version) + f"/channels/{channel_id}"
        response = requests.patch(url, headers=self.headers, json=data)

        response.raise_for_status()

        json_response = response.json()

        logger.debug(f"Successfully modified channel overwrites. Channel now: {json_response}")

        return json_response

    def get_channel_message(self, channel_id: int, message_id: int):
        """Get the message object with the specified ids."""

        url = get_api_url(self.api_version) + f"/channels/{channel_id}/messages/{message_id}"
        response = requests.get(url, headers=self.headers)

        response.raise_for_status()

        json_response = response.json()

        return json_response

    def create_channel_invite(
            self, channel: int | BaseChannel, *, max_age: Optional[int] = None, max_uses: Optional[int] = None,
            temporary: Optional[bool] = None, unique: Optional[bool] = None) -> Invite:
        """Create a channel invite"""

        if isinstance(channel, BaseChannel):
            channel_id = channel.id
        else:
            channel_id = channel

        fields = [(max_age, "max_age"), (max_uses, "max_uses"), (temporary, "temporary"), (unique, "unique")]

        data = {}

        for var, nm in fields:
            if var is not None:
                data[nm] = var

        url = get_api_url(self.api_version) + f"/channels/{channel_id}/invites"

        r = requests.post(url, headers=self.headers, json=data)

        r.raise_for_status()

        return Invite.from_dict(r.json(), client=self)
