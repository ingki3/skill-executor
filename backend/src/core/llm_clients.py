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
        
        # Raw SDK models (kept for compatibility)
        self.flash_model = genai.GenerativeModel('gemini-3-flash-preview')
        self.pro_model = genai.GenerativeModel('gemini-3-pro-preview')

        # LangChain Chat models
        self.simple_model = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=api_key,
            temperature=0
        )
        self.advanced_model = ChatGoogleGenerativeAI(
            model="gemini-3-pro-preview",
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
