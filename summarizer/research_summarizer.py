import os
from infoharvester.embeddings.vector_store import NewsVectorStore
from llm.llm_client import LLMClient

class ResearchSummarizer:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.store = NewsVectorStore()


        # 🔧 system prompt 로딩 (외부 파일)
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "researcher_rag.txt") #Rag with Prompt
        with open(prompt_path, encoding="utf-8") as f:
            self.system_prompt = f.read()

    def summarize(self, symbol: str, query: str, top_k: int = 5) -> dict:
        retrieved_docs = self.store.search(query, k=top_k)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        user_prompt = (
            f"Summarize the following information about {symbol} for an investment analyst:\n\n"
            f"{context}\n\n"
            f"Make sure to identify key developments, risks, and opportunities."
        )

        response = self.llm_client.chat(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt
        )

        return {
            "symbol": symbol,
            "summary": response,
            "sources": [doc.page_content for doc in retrieved_docs]
        }