import base64

from discord.api import DiscordAPI
from exception import BotException

class Emojis:
    @staticmethod
    async def create_emoji(guild_id, name, data):
        try:
            await DiscordAPI.post(f"guilds/{guild_id}/emojis", {
                "name": name,
                "image": base64.b64encode(data).decode("utf-8")
            })
        except Exception:
            raise BotException(":bangbang: Unable to create emoji.")