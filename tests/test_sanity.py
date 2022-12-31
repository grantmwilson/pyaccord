from ..client import Client


def test_sanity():
    client = Client("FAKE BOT TOKEN", api_version=10)
    assert client.api_url == "https://discord.com/api/v10"
