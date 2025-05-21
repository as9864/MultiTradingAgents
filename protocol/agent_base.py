from protocol.message import Message
import os

class AgentBase:
    """
    모든 MCP 에이전트가 상속해야 하는 기본 추상 클래스입니다.
    """
    def __init__(self, name: str):
        self.name = name  # 예: "Trader", "Researcher"

    def handle_message(self, message: Message) -> Message:
        """
        해당 에이전트가 메시지를 처리하고 응답 메시지를 반환합니다.
        :param message: 수신 메시지
        :return: 응답 메시지
        """
        raise NotImplementedError(f"{self.name} agent must implement handle_message()")

    def load_prompt(self, path: str) -> str:
        full_path = os.path.join(os.path.dirname(__file__), '..', path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"[ERROR] Prompt file not found: {full_path}")
            return ""