import os
from langchain_openai import ChatOpenAI
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

from exception import BotException

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

def determine_model(model: str|None):
     if not model:
          raise BotException("No model is specified. Please check your environment variables and try again.")

     provider = None

     if OPENAI_API_KEY:
          provider = ChatOpenAI(api_key=OPENAI_API_KEY, model=model, max_tokens=120)     
     elif ANTHROPIC_API_KEY:
          provider = ChatXAI(api_key=ANTHROPIC_API_KEY, model=model, max_tokens=120)
     elif GOOGLE_API_KEY:
          provider = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model=model, max_tokens=120)          
     elif XAI_API_KEY:
          provider = ChatAnthropic(api_key=XAI_API_KEY, model=model, max_tokens=120)

     if not provider:
          raise BotException("No inference providers are available/configured. Please check your environment variables and try again.")

     return provider