import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class LLMClients:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        
        # Get model names from environment variables
        simple_model_name = os.getenv("MODEL", "gemini-3-flash-preview")
        advanced_model_name = os.getenv("ADVANCED_MODEL", "gemini-2.5-pro")

        # Raw SDK models (kept for compatibility)
        self.flash_model = genai.GenerativeModel(simple_model_name)
        self.pro_model = genai.GenerativeModel(advanced_model_name)

        # LangChain Chat models
        self.simple_model = ChatGoogleGenerativeAI(
            model=simple_model_name,
            google_api_key=api_key,
            temperature=0
        )
        self.advanced_model = ChatGoogleGenerativeAI(
            model=advanced_model_name,
            google_api_key=api_key,
            temperature=0
        )

    async def generate_simple(self, prompt: str) -> str:
        # Use simple_model.ainvoke for consistency if possible
        response = await self.simple_model.ainvoke(prompt)
        return response.content

    async def generate_advanced(self, prompt: str) -> str:
        response = await self.advanced_model.ainvoke(prompt)
        return response.content

llm_clients = LLMClients()
