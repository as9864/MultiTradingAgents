from abc import ABC, abstractmethod
from llm.llm_client import LLMClient
import os

class BaseAgent(ABC):
    """
    모든 역할 기반 Agent들이 상속받는 추상 클래스
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        """
        각 Agent가 실행할 핵심 메서드
        input_data는 컨텍스트, 분석 대상 데이터 등 자유롭게 구성 가능
        """
        pass

    # def load_prompt(self, path: str) -> str:
    #     """
    #     역할별 프롬프트 파일 불러오기
    #     """
    #     try:
    #         with open(path, 'r', encoding='utf-8') as f:
    #             return f.read()
    #     except FileNotFoundError:
    #         print(f"[ERROR] Prompt file not found: {path}")
    #         return ""

    def load_prompt(self, path: str) -> str:
        full_path = os.path.join(os.path.dirname(__file__), '..', path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"[ERROR] Prompt file not found: {full_path}")
            return ""