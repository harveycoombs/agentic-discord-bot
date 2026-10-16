from discord.api import DiscordAPI
from exception import BotException

class Roles:
    @staticmethod
    async def get_roles(guild_id):
        try:
            roles = await DiscordAPI.get(f"guilds/{guild_id}/roles")
            return roles
        except Exception:
            raise BotException(":bangbang: Unable to retrieve roles.")

    @staticmethod
    async def get_role(guild_id, role_id):
        try:
            role = await DiscordAPI.get(f"guilds/{guild_id}/roles/{role_id}")
            return role
        except Exception:
            raise BotException(":bangbang: Unable to retrieve role.")
    
    @staticmethod
    async def create_role(guild_id, name, color=0, hoist=False, mentionable=False, permissions=0):
        try:
            await DiscordAPI.post(f"guilds/{guild_id}/roles", {
                "name": name,
                "color": color,
                "hoist": hoist,
                "mentionable": mentionable,
                "permissions": permissions
            })
        except Exception:
            raise BotException(":bangbang: Unable to create role.")
        
    @staticmethod
    async def delete_role(guild_id, role_id):
        try:
            await DiscordAPI.delete(f"guilds/{guild_id}/roles/{role_id}")
        except Exception:
            raise BotException(":bangbang: Unable to delete role.")

    @staticmethod
    async def add_role_to_user(guild_id, user_id, role_id):
        try:
            await DiscordAPI.put(f"guilds/{guild_id}/members/{user_id}/roles/{role_id}", payload=None)
        except Exception:
            raise BotException(":bangbang: Unable to add role to user.")

    @staticmethod
    async def remove_role_from_user(guild_id, user_id, role_id):
        try:
            await DiscordAPI.delete(f"guilds/{guild_id}/members/{user_id}/roles/{role_id}", payload=None)
        except Exception:
            raise BotException(":bangbang: Unable to remove role from user.")