import os
import json

from data import get_guild_interaction_count, get_registered_guild_owner, set_guild_interaction_count, register_guild, guild_is_registered, insert_error_log, update_registered_guild_owner, get_model_choice, get_user_api_keys
from discord.messages import Messages
from ai.agent import Agent
from exception import BotException
from discord.guilds import Guilds
from discord.utils import Utils
from ai.direct import generate_response_to_image
from ai.models import determine_model

class Events:
    @staticmethod
    async def handle(raw):
        event = json.loads(raw)

        event_type = event["t"]
        event_data = event["d"]

        match event_type:
            case "READY":
                print(f"Bot is ready in {len(event_data['guilds'])} guilds.")
                return

            case "MESSAGE_CREATE":
                author_id = event_data["author"]["id"]
                channel_id = event_data["channel_id"]
                guild_id = event_data["guild_id"]

                if author_id == os.getenv("APPLICATION_ID") or os.getenv("APPLICATION_ID") not in [mention["id"] for mention in event_data["mentions"]]:
                    return

                guild_id = event_data["guild_id"]

                try:
                    if len(event_data["attachments"]) > 0:
                        response = generate_response_to_image(
                             event_data["content"].replace(f"<@!{os.getenv('APPLICATION_ID')}>", "").strip(), 
                             event_data["attachments"][0]["url"]
                        )
                        await Messages.create_message(channel_id, response[:2000])
                        return

                    agent = Agent(context=event_data)
                    response = await agent.respond(event_data["content"].replace(f"<@!{os.getenv('APPLICATION_ID')}>", "").strip())

                    if len(response) > 2000:
                        for x in range(0, len(response), 2000):
                            await Messages.create_message(channel_id, response[x:x+2000])
                    else:
                        await Messages.create_message(channel_id, response)
                except BotException as ve:
                    await Messages.create_message(channel_id, str(ve))
                    return
                except Exception as e:
                    insert_error_log(guild_id, author_id, event_data["content"], str(e))
                    await Messages.create_message(channel_id, ":bangbang: Something went wrong.")
                    return
                
            case "GUILD_CREATE":
                guild_id = event_data["id"]
                owner_id = event_data["owner_id"]

                if not guild_is_registered(guild_id):
                    register_guild(guild_id, owner_id)

                    system_channel_id = event_data["system_channel_id"]

                    await Messages.create_message(system_channel_id, None, [{
                        "title": ":wave: Thank you for inviting me to your server!",
                        "description": "Ask me what I can do, to get started.",
                        "color": Messages.embed_color
                    }], [{
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "Donate",
                                "style": 5,
                                "url": "https://buymeacoffee.com/harveycoombs"
                            }
                        ]
                    }])
                    return
                else:
                    update_registered_guild_owner(guild_id, owner_id)

            case "GUILD_UPDATE":
                update_registered_guild_owner(event_data["guild_id"], event_data["owner_id"])
                return

            case "GUILD_MEMBER_REMOVE":
                member = event_data["user"]

                guild = await Guilds.get_guild(event_data["guild_id"])
                system_channel_id = guild["system_channel_id"]

                avatar_url = f"https://cdn.discordapp.com/avatars/{member['id']}/{member['avatar']}.webp"
                creation_date = Utils.snowflake_to_datetime(int(member["id"]))

                await Messages.create_message(system_channel_id, None, [{
                    "title": f":outbox_tray: {member['global_name']} left the server",
                    "description": f"Joined Discord on `{creation_date}`",
                    "author": {
                        "name": member["username"] or "Unknown User",
                        "icon_url": avatar_url
                    },
                    "thumbnail": {
                        "url": avatar_url
                    },
                    "footer": {
                        "text": f"{guild['name']} now has {guild['approximate_member_count'] or "?"} members",
                        "icon_url": f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.webp"
                    },
                    "color": Messages.embed_color
                }])
                return

            case "GUILD_MEMBER_ADD":
                member = event_data["user"]

                guild = await Guilds.get_guild(event_data["guild_id"])
                system_channel_id = guild["system_channel_id"]

                avatar_url = f"https://cdn.discordapp.com/avatars/{member['id']}/{member['avatar']}.webp"
                creation_date = Utils.snowflake_to_datetime(int(member["id"]))

                await Messages.create_message(system_channel_id, None, [{
                    "title": f":inbox_tray: {member['global_name'] or member['username']} joined the server",
                    "description": f"Joined Discord on `{creation_date}`",
                    "author": {
                        "name": member["username"] or "Unknown User",
                        "icon_url": avatar_url
                    },
                    "thumbnail": {
                        "url": avatar_url
                    },
                    "footer": {
                        "text": f"{guild['name']} now has {guild['approximate_member_count'] or "?"} members",
                        "icon_url": f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.webp"
                    },
                    "color": Messages.embed_color
                }])
                return