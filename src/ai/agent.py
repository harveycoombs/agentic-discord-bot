import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

from ai.toolchain import get_bot_creator, get_server_info, add_role, remove_role, create_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message, ban_member, unban_member, kick_member, bulk_delete_messages, rename_channel, get_server_interaction_count, generate_image_from_prompt, create_server_invite, delete_server_invite, update_server, summarise_channel_messages

class Agent:
    def __init__(self, context: dict, model: str, api_keys: dict):
        self.context = context
        self.api_keys = api_keys

        if model.startswith("gpt-"):
            self.model = ChatOpenAI(api_key=api_keys["openai_api_key"], model=model, max_tokens=120)
        elif model.startswith("grok-"):
            self.model = ChatXAI(api_key=api_keys["xai_api_key"], model=model, max_tokens=120)
        elif model.startswith("gemini-"):
            self.model = ChatGoogleGenerativeAI(api_key=api_keys["google_api_key"], model=model, max_tokens=120)
        elif model.startswith("claude-"):
            self.model = ChatAnthropic(api_key=api_keys["anthropic_api_key"], model=model, max_tokens=120)
        else:
            self.model = model

        self.agent = create_agent(
            model=self.model,
            tools=[get_bot_creator, get_server_info, add_role, remove_role, create_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message, ban_member, unban_member, kick_member, bulk_delete_messages, rename_channel, get_server_interaction_count, generate_image_from_prompt, create_server_invite, delete_server_invite, update_server, summarise_channel_messages],
            system_prompt=f"You are a helpful assistant created by Harvey Coombs that decides which tool is most appropriate to use based on the user's prompt, using both the user's prompt and the following data as parameters for each tool: {json.dumps(self.context)}. You absolutely must keep your responses concise, and they must not exceed 120 tokens.",
        )

    async def respond(self, prompt: str):
        response = await self.agent.ainvoke({ "messages": [{ "role": "user", "content": prompt }]})

        print(response)
        
        return response["messages"][-1].content