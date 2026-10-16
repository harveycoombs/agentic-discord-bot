import json
import os
import aiohttp

from discord.roles import Roles
from discord.members import Members
from discord.channels import Channels
from discord.messages import Messages
from discord.permissions import Permissions
from discord.guilds import Guilds
from exception import BotException
from data import get_guild_interaction_count
from ai.images import generate_image
 
def get_bot_creator() -> str:
    """Gets the creator of you, the bot."""
    return "[Harvey Coombs](https://harveycoombs.com)"

async def get_server_info(guild_id: str) -> str:
    """Gets information about the current server."""
    guild = await Guilds.get_guild(guild_id)
    return json.dumps(guild)

async def add_role(role_name: str, guild_id: str, message_author_id: str, target_user_id: str|None = None) -> str:
    """Adds a role to another user. Input should be a string with the role's name, a string with the guild's ID, a string with the message author's ID and an optional string with the target user's ID."""
    guild = await Guilds.get_guild(guild_id)
    roles = await Roles.get_roles(guild_id)
    author = await Members.get_member(guild_id, message_author_id)

    member_roles = [role for role in roles if role["id"] in author["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to assign roles.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_ROLES) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to assign roles.")

    role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

    if role is None:
        raise BotException(":warning: The provided role does not exist.")
    
    await Roles.add_role_to_user(guild_id, message_author_id if target_user_id is None else target_user_id, role["id"])
    return f":white_check_mark: I have added the '{role_name}' role."

async def remove_role(role_name: str, guild_id: str, author_id: str, target_id: str = None) -> str:
    """Removes a role from another user. Input should be a string with the role's name."""
    roles = await Roles.get_roles(guild_id)
    role = None

    try:
        role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)
    except:
        role = None

    if role is None:
        raise BotException(f":warning: The provided role does not exist.")
    
    await Roles.remove_role_from_user(guild_id, author_id if target_id is None else target_id, role["id"])
    return f":white_check_mark: I have removed the '{role_name}' role."

async def create_role(role_name: str, role_color: str, guild_id: str, author_id: str) -> str:
    """Creates a role. Input should be a string with the role's name and a string with the role's color."""
    color_hex = role_color.replace("#", "").replace("\"", "").strip()
    safe_role_name = role_name.strip("\"").strip()

    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to create roles.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_ROLES) or guild["owner_id"] == author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to create roles.")

    await Roles.create_role(guild_id, safe_role_name, int(color_hex, 16))
    return f":white_check_mark: I have created the '{safe_role_name}' role."

async def change_nickname(nickname: str, guild_id: str, target_user_id: str) -> str:
    """Changes the nickname of a user. Input should be a string with the new nickname and a string with the target user's ID."""
    await Members.update_member(guild_id, target_user_id, nickname)
    return f":white_check_mark: I have changed your nickname to '{nickname}'."

async def create_text_channel(channel_name: str, guild_id: str, message_author_id: str, category_name: str = None) -> str:
    """Creates a text channel. Input should be a string with the channel's name and optionally a string with the category's name."""
    print(channel_name, guild_id, message_author_id, category_name)

    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to create channels.")

    new_channel_id = await Channels.create_channel(guild_id, channel_name, 0, category_name)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def create_voice_channel(channel_name: str, guild_id: str, message_author_id: str, category_name: str = None) -> str:
    """Creates a voice channel. Input should be a string with the channel's name and optionally a string with the category's name."""
    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to create channels.")
        
    new_channel_id = await Channels.create_channel(guild_id, channel_name, 2, category_name)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def delete_channel(channel_name: str, guild_id: str, author_id: str) -> str:
    """Deletes a channel. Input should be a string with the channel's name."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to delete channels.")
        
    channels = await Channels.get_channels(guild_id)
    channel = next((channel for channel in channels if channel["name"].strip().lower() == channel_name.strip().lower()), None)

    if channel is None:
        raise BotException(f":warning: The provided channel does not exist.")

    await Channels.delete_channel(channel["id"])
    return f":white_check_mark: I have deleted the '{channel_name}' channel."

async def rename_channel(guild_id: str, channel_name: str, new_name: str, message_author_id: str) -> str:
    """Renames a channel. Input should be a string with the channel's name and a string with the new name."""

    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to rename channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to rename channels.")

    channels = await Channels.get_channels(guild_id)
    channel = next((channel for channel in channels if channel["name"].strip().lower() == channel_name.strip().lower()), None)

    if channel is None:
        raise BotException(f":warning: The provided channel does not exist.")

    await Channels.rename_channel(channel["id"], new_name)
    return f":white_check_mark: I have renamed the <#{channel['id']}> channel to '{new_name}'."

async def delete_message(channel_id: str, message_id: str, guild_id: str, author_id: str) -> str:
    """Deletes a message. Input should be a string with the message's ID.""" 
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_MESSAGES) or guild["owner_id"] == author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to delete messages.")
        
    await Messages.delete_message(channel_id, message_id)
    return ":white_check_mark: I have deleted the referenced message."

async def bulk_delete_messages(amount: int, channel_id: str, guild_id: str, author_id: str) -> str:
    """Bulk deletes messages in the current channel. Input should be a number with the amount of messages to delete."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_MESSAGES) or guild["owner_id"] == author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to delete messages.")
        
    await Messages.bulk_delete_messages(channel_id, amount)
    return f":white_check_mark: I have deleted {amount} messages."

async def ban_member(member_id: str, reason: str, guild_id: str, author_id: str) -> str:
    """Bans a member. Input should be a string with the reason for the ban."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to ban members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.BAN_MEMBERS) or guild["owner_id"] == author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to ban members.")
        
    await Members.ban_member(guild_id, member_id, reason)
    return f":white_check_mark: I have banned <@{member_id}>."

async def unban_member(member_id: str, guild_id: str, author_id: str) -> str:
    """Unbans a member. Input should be a string with the member's ID."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to unban members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.BAN_MEMBERS) or guild["owner_id"] == author_id:
            break
    await Members.unban_member(guild_id, member_id)
    return f":white_check_mark: I have unbanned <@{member_id}>."

async def kick_member(member_id: str, guild_id: str, author_id: str) -> str:
    """Kicks a member. Input should be a string with the member's ID."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise BotException(":no_entry_sign: You do not have permission to kick members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.KICK_MEMBERS) or guild["owner_id"] == author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to kick members.")
        
    await Members.remove_member(guild_id, member_id)
    return f":white_check_mark: I have kicked <@{member_id}>."

async def get_server_interaction_count(guild_id: str) -> int:
    """Gets the interaction count for the current server."""
    interactions = get_guild_interaction_count(guild_id)
    return interactions

async def generate_image_from_prompt(prompt: str, guild_id: str) -> str:
    """Generates an image. Input should be a string with the prompt. The output should be a string with the image's URL. You should only respond with the image's URL."""
    output_path = os.path.join(os.getcwd(), f"result_{guild_id}.png")
    generate_image(prompt, output_path)

    with open(output_path, "rb") as image_file:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://agenti.bot/api/user/servers/{guild_id}/images", data={ "file": image_file }) as response:
                if response.status >= 400:
                    raise BotException(await response.text())

                result = await response.json()

                return result["url"]

async def create_server_invite(channel_id: str, age: int, temporary: bool, guild_id: str, message_author_id: str) -> str:
    """Creates a server invite. Input should be a string with the channel's ID, an integer with the age limit in seconds, a boolean with whether the invite is temporary, a string with the guild's ID and a string with the message author's ID."""
    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.CREATE_INSTANT_INVITE) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to create invites.")

    invite_code = await Channels.create_invite(channel_id, age, temporary)
    return f":white_check_mark: I have created an invite for this channel, here is the URL: https://discord.gg/{invite_code}"

async def delete_server_invite(invite_code: str, channel_id: str, guild_id: str, message_author_id: str) -> str:
    """Deletes a server invite. Input should be a string with the invite's code, a string with the channel's ID, a string with the guild's ID and a string with the message author's ID."""
    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.CREATE_INSTANT_INVITE) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to create invites.")

    await Channels.delete_invite(channel_id, invite_code)
    return f":white_check_mark: I have deleted the invite '{invite_code}' for this channel."

async def update_server(guild_id: str, message_author_id: str, name: str = None, description: str = None) -> str:
    """Updates the server. Input should be a string with the guild's ID, a string with the message author's ID, an optional string with the new name and an optional string with the new description."""
    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise BotException(":no_entry_sign: You do not have permission to update the server.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_GUILD) or guild["owner_id"] == message_author_id:
            break
        else:
            raise BotException(":no_entry_sign: You do not have permission to update the server.")

    await Guilds.update_guild(guild_id, {
        "name": name,
        "description": description
    })
    
    return ":white_check_mark: I have updated the server."

async def summarise_channel_messages(channel_id: str, limit: int = 50) -> str:
    """Retrieves a list of the most recent messages in a specified channel, for use when generating a concise summary in the form of a paragraph. Input should be a string with the channel's ID and an optional integer with the number of messages to retrieve."""
    messages = await Messages.get_messages(channel_id, limit)

    clean_messages = list(map(lambda message: {
        "content": f"{message['content'][:200]} ... {message['content'][-50:]}" if len(message["content"]) > 250 else message["content"],
        "author": message["author"]["username"],
        "timestamp": message["timestamp"]
    }, messages))

    return json.dumps(clean_messages)