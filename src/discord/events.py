import os
import json

from data import get_guild_interaction_count, get_registered_guild_owner, set_guild_interaction_count, register_guild, guild_is_registered, insert_error_log, update_registered_guild_owner, get_model_choice, get_user_api_keys
from kv import get_kv, set_kv
from discord.messages import Messages
from ai.agent import Agent
from exception import BotException
from discord.guilds import Guilds
from discord.utils import Utils
from ai.direct import generate_response_to_image

class Events:
    @staticmethod
    async def handle(raw):
        event = json.loads(raw)

        event_type = event["t"]
        event_data = event["d"]

        match event_type:
            case "READY":
                set_kv("guild_count", len(event_data["guilds"]))
                print(f"Bot is ready in {len(event_data['guilds'])} guilds.")
                return

            case "MESSAGE_CREATE":
                author_id = event_data["author"]["id"]
                channel_id = event_data["channel_id"]
                guild_id = event_data["guild_id"]

                model = get_model_choice(guild_id)

                if author_id == os.getenv("APPLICATION_ID") or os.getenv("APPLICATION_ID") not in [mention["id"] for mention in event_data["mentions"]]:
                    return

                guild_id = event_data["guild_id"]

                interaction_count = get_guild_interaction_count(guild_id)
                set_guild_interaction_count(guild_id, interaction_count + 1)

                owner_id = get_registered_guild_owner(guild_id)


                api_keys = get_user_api_keys(owner_id) if owner_id else None
               
                if not api_keys:
                    await Messages.create_message(channel_id, ":bangbang: No API keys are configured for this server. If you are the owner, please configure your API keys in your [account settings](https://agenti.bot/manage).")
                    return
                
                try:
                    if len(event_data["attachments"]) > 0:
                        response = generate_response_to_image(
                             api_keys["openai_api_key"],
                             api_keys["xai_api_key"],
                             api_keys["google_api_key"],
                             api_keys["anthropic_api_key"],
                             model, 
                             event_data["content"].replace(f"<@!{os.getenv('APPLICATION_ID')}>", "").strip(), 
                             event_data["attachments"][0]["url"]
                        )
                        await Messages.create_message(channel_id, response[:2000])
                        return

                    agent = Agent(context=event_data, model=model, api_keys=api_keys)
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
                    await Messages.create_message(channel_id, ":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                    return
                
            case "GUILD_CREATE":
                guild_id = event_data["id"]
                owner_id = event_data["owner_id"]

                if not guild_is_registered(guild_id):
                    register_guild(guild_id, owner_id)

                    system_channel_id = event_data["system_channel_id"]

                    set_kv("guild_count", get_kv("guild_count") + 1)

                    await Messages.create_message(system_channel_id, None, [{
                        "title": ":wave: Thank you for inviting me to your server!",
                        "description": "Check out the [About page](https://www.agenti.bot/about) to get started.",
                        "color": Messages.embed_color
                    }], [{
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "Website",
                                "style": 5,
                                "url": "https://www.agenti.bot"
                            },
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
            
            case "GUILD_DELETE":
                set_kv("guild_count", get_kv("guild_count") - 1)
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