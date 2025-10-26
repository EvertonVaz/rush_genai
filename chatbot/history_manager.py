from typing import List
from chatbot.database import MessageRepository
from chatbot.schemas import PromptData, MessageData, SummaryData
from chatbot.prompts import PromptGenerator



class HistoryManager:
    def __init__(self):
        self.message_repository = MessageRepository()
        self.prompt_data: PromptData = self.update_prompt_data()

    def get_chat_history(self, limit: int = 5) -> str:
        result: List[MessageData] = self.message_repository.get_recent_messages(n=limit)
        return "\n".join([f"{msg.role}: {msg.content}" for msg in result])

    def get_summaries(self, limit: int = 5) -> str:
        result: List[SummaryData] = self.message_repository.get_lasts_summary()
        return "\n".join(
            [f"{summary.content}" for summary in result[:limit]] if result else ""
        )

    def update_prompt_data(self, user_input: str = "") -> PromptData:
        data: PromptData = PromptData(
            user_input=user_input,
            history=self.get_chat_history(),
            summarys=self.get_summaries(),
            messages_count=self.message_repository.get_total_messages_count(),
        )
        print(f"Historico:\n{data.history}\nResumos:\n{data.summarys}\n")
        return data




