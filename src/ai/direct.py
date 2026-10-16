from openai import OpenAI

from exception import BotException

def generate_response_to_image(openai_api_key: str, xai_api_key: str, google_api_key: str, anthropic_api_key: str, model: str, prompt: str, attachment_url: str) -> str:
     openai_client = OpenAI(api_key=openai_api_key)
     xai_client = OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")
     gemini_client = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai")
     anthropic_client = OpenAI(api_key=anthropic_api_key, base_url="https://api.anthropic.com/v1")

     client = openai_client if model.startswith("gpt-") else xai_client if model.startswith("grok-") else gemini_client if model.startswith("gemini-") else anthropic_client if model.startswith("claude-") else None
     
     if not client:
          raise BotException(f"Unable to determine provided model '{model}'.")
     
     response = client.responses.create(
          model=model,
          input=[{
               "role": "user", 
               "content": [{
                    "type": "input_text", 
                    "text": prompt 
               }, 
               { 
                    "type": "input_image", 
                    "image_url": attachment_url 
               }]
          }]
     )
     
     return response.output_text