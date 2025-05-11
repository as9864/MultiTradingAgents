import os
from openai import OpenAI
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LLMClient:
    def __init__(self, model: str = "gpt-4-turbo"):
        self.model = model
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def chat(self, system_prompt: str, user_prompt: str, messages: Optional[List[dict]] = None, temperature: float = 0.7) -> str:
        messages = messages or []
        full_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ] + messages

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return "[ERROR] Failed to retrieve response from LLM."

    def summarize(self, text: str) -> str:
        system_prompt = "You are a helpful assistant that summarizes financial documents."
        user_prompt = f"Summarize the following text:\n{text}"
        return self.chat(system_prompt, user_prompt)