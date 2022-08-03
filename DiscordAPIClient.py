"""API calls for performing Discord API actions."""

from __future__ import annotations

from typing import Dict, List, Optional, Union
import requests
import logging

from pyaccord.types.guild import Guild
from pyaccord.types.user import CurrentUser, User
from .url_functions import get_api_url

logger = logging.getLogger("DiscordAPI")


class DiscordAPIClient:
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

    def get_guild(self, id: int) -> Optional[Guild]:
        """Get a guild by id"""

        url = self.api_url + f"/guilds/{id}"
        r = requests.get(url, headers=self.headers)

        if not r.ok:
            logger.error(f"{r.content}")
        r.raise_for_status()

        json_response = r.json()

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

        guilds = Guild.from_list_of_dict(r.json())

        logger.debug(f"Got current user guilds: {guilds}")

        return guilds

    # endregion

    # endregion

    def create_guild_role(self, guild_id: int, *,
                          name: Optional[str] = None,
                          permissions: Optional[int] = None,
                          color: Optional[int] = None,
                          hoist: Optional[bool] = False,
                          mentionable: Optional[bool] = False) -> int:
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

        json_response = response.json()

        role_id = json_response["id"]
        role_name = json_response["name"]

        logger.info(f"Created new guild role {role_name} with snowflake: {role_id}")

        return role_id

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
