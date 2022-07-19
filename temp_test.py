DISCORD_CLIENT_ID = r"837501631306268704"
DISCORD_CLIENT_SECRET = r"kwGfE3HfSjDi0C19F14uCO1IIbN5qUNL"
BOT_TOKEN = r"ODgxMjExMTUxOTE5MjQ3NDIx.YSph1g.Z2wRK-vNg19rm0BDC0TRSbKtUuU"
PRODUCTION_BOT_TOKEN = r"ODgxMjExMTUxOTE5MjQ3NDIx.YSph1g.Z2wRK-vNg19rm0BDC0TRSbKtUuU"
GUILD_ID = 731598642426675301

import sys

sys.path.append("C:\\Users\\Grant\\Documents\\Repositories\\EngFrosh-Organization\\engfrosh")

from engfrosh_common.DiscordAPI.DiscordAPI import DiscordAPI

# api = DiscordAPI(BOT_TOKEN, api_version=9)
api = DiscordAPI(PRODUCTION_BOT_TOKEN, api_version=9)

# CHANNEL_ID = 731598642426675305

# # channel = api.get_channel(731598642426675305)

# # print(channel)

# # permissions = api.get_channel_overwrites(731598642426675305)

# # print(permissions)

# res = api.modify_channel_overwrites(CHANNEL_ID, {
#     "id": 881968479752826990,
#     "allow": 1024,
#     "deny": 0
# })

res = api.get_channel_message(882653357272096788, 882659706076790854)
# res = api.get_channel(882653357272096788)

print(res)
