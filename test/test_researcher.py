from agents.researcher_agent import ResearcherAgent
from llm.llm_client import LLMClient


def test_researcher():
    llm = LLMClient(model="gpt-4-turbo")
    agent = ResearcherAgent(llm)

    example_input = {
        "company_name": "Apple Inc.",
        "document": (
            "Apple Inc. announced its Q1 earnings showing a revenue increase of 12% YoY. "
            "Mac sales rose sharply while iPhone sales slightly declined. "
            "The company highlighted strong growth in services. "
            "However, supply chain issues in China remain a concern."
        )
    }

    result = agent.run(example_input)



    print(f"\n📊 ResearcherAgent Result:")
    print(f"Company: {result['company']}")
    print(f"Summary:\n{result['summary']}")

if __name__ == "__main__":
    test_researcher()