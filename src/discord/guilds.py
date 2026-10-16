from discord.api import DiscordAPI
from exception import BotException

class Guilds:
    @staticmethod
    async def get_guilds():
        try:
            guilds = await DiscordAPI.get("users/@me/guilds")
            return guilds
        except Exception:
            raise BotException(":bangbang: Unable to retrieve servers.")

    @staticmethod
    async def get_guild(guild_id):
        try:
            guild = await DiscordAPI.get(f"guilds/{guild_id}?with_counts=true")
            return guild
        except Exception:
            raise BotException(":bangbang: Unable to retrieve server.")

    @staticmethod
    async def update_guild(guild_id, params):
        try:
            await DiscordAPI.patch(f"guilds/{guild_id}", params)
        except Exception:
            raise BotException(":bangbang: Unable to update server.")

    @staticmethod
    async def leave_guild(guild_id):
        try:
            await DiscordAPI.delete(f"users/@me/guilds/{guild_id}")
        except Exception:
            raise BotException(":bangbang: Unable to leave server.")