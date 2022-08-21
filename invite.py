
from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import Client


class Invite:

    code: str
    _client: Optional[Client]

    @property
    def full_url(self) -> str:
        return f"https://discord.gg/{self.code}"

    def __init__(self, code: str, *, client: Optional[Client] = None) -> None:
        self.code = code
        self._client = client

    @staticmethod
    def from_dict(d: Dict, *, client: Optional[Client] = None) -> Invite:
        return Invite(
            code=d["code"],
            client=client
        )
