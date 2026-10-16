from discord.api import DiscordAPI
from exception import BotException

class Members:
    @staticmethod
    async def get_members(guild_id):
        try:
            members = await DiscordAPI.get(f"guilds/{guild_id}/members")
            return members
        except Exception as ex:
            print(ex)
            raise BotException(":bangbang: Unable to retrieve members.")
        
    @staticmethod
    async def get_member(guild_id, user_id):
        try:
            member = await DiscordAPI.get(f"guilds/{guild_id}/members/{user_id}")
            return member
        except Exception as ex:
            print(ex)
            raise BotException(":bangbang: Unable to retrieve member.")
    
    @staticmethod
    async def update_member(guild_id, user_id, nickname):
        await DiscordAPI.patch(f"guilds/{guild_id}/members/{user_id}", {
            "nick": nickname
        })
    
    @staticmethod
    async def remove_member(guild_id, user_id):
        try:
            await DiscordAPI.delete(f"guilds/{guild_id}/members/{user_id}")
        except Exception as ex:
            print(ex)
            raise BotException(":bangbang: Unable to remove member.")

    @staticmethod
    async def ban_member(guild_id, user_id, reason):
        try:
            await DiscordAPI.put(f"guilds/{guild_id}/bans/{user_id}", {
                "reason": reason
            })
        except Exception as ex:
            print(ex)
            raise BotException(":bangbang: Unable to ban member.")

    @staticmethod
    async def unban_member(guild_id, user_id):
        try:
            await DiscordAPI.delete(f"guilds/{guild_id}/bans/{user_id}")
        except Exception as ex:
            print(ex)
            raise BotException(":bangbang: Unable to unban member.")