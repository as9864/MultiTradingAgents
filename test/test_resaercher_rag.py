from agents.researcher_agent import ResearcherAgent
from llm.llm_client import LLMClient

def test_rag_researcher():
    llm = LLMClient()
    agent = ResearcherAgent(llm)


    result = agent.run({
        "symbol": "AAPL",
        "query": "Apple's market outlook"
    })

    print("📌 Summary:\n", result["summary"])
    print("\n📚 Sources:\n")
    for s in result["sources"]:
        print("-", s.split('\n')[0])

if __name__ == "__main__":
    test_rag_researcher()