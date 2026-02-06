import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClients:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        
        # We'll use the raw SDK for simple calls and can use LangChain wrappers later if needed
        # Use gemini-3 preview models as requested
        self.flash_model = genai.GenerativeModel('gemini-3-flash-preview')
        self.pro_model = genai.GenerativeModel('gemini-3-pro-preview')

    async def generate_simple(self, prompt: str) -> str:
        response = self.flash_model.generate_content(prompt)
        return response.text

    async def generate_advanced(self, prompt: str) -> str:
        response = self.pro_model.generate_content(prompt)
        return response.text

llm_clients = LLMClients()
