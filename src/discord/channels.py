from discord.api import DiscordAPI
from exception import BotException

class Channels:
    @staticmethod
    async def get_channels(guild_id):
        try:
            channels = await DiscordAPI.get(f"guilds/{guild_id}/channels")
            return channels
        except Exception:
            raise BotException(":bangbang: Unable to retrieve channels.")

    @staticmethod
    async def get_channel_categories(guild_id):
        try:
            categories = await DiscordAPI.get(f"guilds/{guild_id}/channels?type=4")
            return categories
        except Exception:
            raise BotException(":bangbang: Unable to retrieve channel categories.")

    @staticmethod
    async def create_channel(guild_id, channel_name, channel_type=0, category_name=None):
        categories = await Channels.get_channel_categories(guild_id)
        category_id = next(category["id"] for category in categories if category["name"].strip().lower() == category_name.strip().lower()) if category_name else None

        try:
            response = await DiscordAPI.post(f"guilds/{guild_id}/channels", {
                "name": channel_name,
                "type": channel_type,
                "parent_id": category_id
            })

            return response["id"]
        except Exception as ex:
            print(ex)
            raise BotException(":bangbang: Unable to create channel.")
        
    @staticmethod
    async def rename_channel(channel_id, new_name):
        try:
            await DiscordAPI.patch(f"channels/{channel_id}", {
                "name": new_name
            })
        except Exception:
            raise BotException(":bangbang: Unable to rename channel.")

    @staticmethod
    async def delete_channel(channel_id):
        try:
            await DiscordAPI.delete(f"channels/{channel_id}")
        except Exception:
            raise BotException(":bangbang: Unable to delete channel.")

    @staticmethod
    async def create_invite(channel_id, age, temporary):
        try:
            invitation = await DiscordAPI.post(f"channels/{channel_id}/invites", {
                "max_age": age,
                "temporary": temporary
            })
            return invitation["code"]
        except Exception:
            raise BotException(":bangbang: Unable to create channel invite.")

    @staticmethod
    async def delete_invite(channel_id, invite_code):
        try:
            await DiscordAPI.delete(f"channels/{channel_id}/invites/{invite_code}")
        except Exception:
            raise BotException(":bangbang: Unable to delete channel invite.")