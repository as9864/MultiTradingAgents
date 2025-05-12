from protocol.message import Message
from protocol.agent_base import AgentBase

class MessageRouter:
    """
    Agent 간 메시지를 중재하고 전달하는 MCP 메시지 라우터입니다.
    """

    def __init__(self, agents: dict):
        """
        :param agents: {"Trader": TraderAgent, "Researcher": ResearcherAgent, ...}
        """
        self.agents = agents
        self.shared_state = {}  # 선택적으로 Agent 간 공유되는 상태 저장

    def dispatch(self, message: Message) -> Message:
        """
        메시지를 대상 Agent에게 전달하고 응답을 반환합니다.
        :param message: Message 인스턴스
        :return: 응답 메시지 (Message)
        """
        print(f"📨 Dispatch: {message.summary()}")

        receiver = self.agents.get(message.receiver)
        if receiver and isinstance(receiver, AgentBase):
            response = receiver.handle_message(message)
            return response
        else:
            return Message(
                sender="Router",
                receiver=message.sender,
                type="error",
                content={"error": f"Unknown agent: {message.receiver}"}
            )