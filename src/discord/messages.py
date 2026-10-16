import os
import asyncio

from discord.api import DiscordAPI
from exception import BotException

class Messages:
    embed_color = os.getenv("EMBED_COLOR")

    @staticmethod
    async def get_messages(channel_id: str, limit: int = 50):
        try:
            messages = await DiscordAPI.get(f"channels/{channel_id}/messages?limit={limit}")
            return messages
        except Exception:
            raise BotException(":bangbang: Unable to retrieve messages.")

    @staticmethod    
    async def create_message(channel_id, content, embeds=None, components=None):
        print(f"content: {content}")

        if not content and not embeds:
            content = "Sorry, I didn't understand that. Please try again or [Contact Support](https://www.agenti.bot/contact) if this issue persists."

        try:
            await DiscordAPI.post(f"channels/{channel_id}/messages", {
                "content": content,
                "tts": False,
                "embeds": embeds or [],
                "components": components or []
            })
        except Exception as e:
            print(e)
            raise BotException(f":bangbang: Unable to create message ({e}).")

    @staticmethod
    async def update_message(channel_id, message_id, content=None, embeds=None):
        try:
            await DiscordAPI.patch(f"channels/{channel_id}/messages/{message_id}", {
                "content": content,
                "embeds": embeds or []
            })
        except Exception:
            raise BotException(":bangbang: Unable to update message.")

    @staticmethod
    async def delete_message(channel_id, message_id):
        try:
            await DiscordAPI.delete(f"channels/{channel_id}/messages/{message_id}")
        except Exception:
            raise BotException(":bangbang: Unable to delete message.")

    @staticmethod
    async def bulk_delete_messages(channel_id, amount):
        try:
            messages = await DiscordAPI.get(f"channels/{channel_id}/messages")

            for x in range(int(amount) + 1):
                await DiscordAPI.delete(f"channels/{channel_id}/messages/{messages[x]['id']}")
                await asyncio.sleep(0.75)
        except Exception:
            raise BotException(":bangbang: Unable to bulk delete messages.")