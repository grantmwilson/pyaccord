from pyaccord import Client


def test_client_sanity():
    client = Client("FAKE BOT TOKEN", api_version=10)
    assert client.api_url == "https://discord.com/api/v10"
