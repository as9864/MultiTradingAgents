import uuid
from datetime import datetime

class Message:
    def __init__(
        self,
        sender: str,
        receiver: str,
        type: str,
        content: dict,
        message_id: str = None,
        timestamp: str = None
    ):
        """
        :param sender: 메시지를 보내는 agent 이름
        :param receiver: 메시지를 받는 agent 이름
        :param type: 메시지 타입 ("request", "response", "feedback" 등)
        :param content: 메시지 내용 (딕셔너리)
        :param message_id: 메시지 고유 ID (자동 생성 가능)
        :param timestamp: 메시지 생성 시간 (ISO8601)
        """
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.content = content
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def __repr__(self):
        return f"<{self.type.upper()} from {self.sender} to {self.receiver} @ {self.timestamp}>"

    def summary(self) -> str:
        return f"[{self.type}] {self.sender} → {self.receiver} | {list(self.content.keys())}"