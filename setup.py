from distutils.core import setup

setup(name="pyaccord", version="0.0.1",
      py_modules=["channel", "client", "DiscordMessage", "DiscordUserAPI", "exceptions", "guild", "invite",
                  "permissions", "role", "url_functions", "user"], install_requires=["requests(>=2.28.0)"])
