from typing import List
from google import genai
from google.genai import types

from chatbot.database import MessageRepository, UserRepository
from chatbot.schemas import PromptData, ResponseData, RoleType
from chatbot.schemas import Movie
from chatbot.func_declarations import function_declarations
from chatbot.prompts import PromptGenerator

from dotenv import load_dotenv

load_dotenv()


class PersistentChatbot:

    def __init__(self):
        self.msg_repo = MessageRepository()
        self.user_movies = UserRepository()
        self.prompt_gen = PromptGenerator()
        self.prompt_data = PromptData(
            chat_history=self.msg_repo.get_last_n_messages(n=5),
            summary_list=self.msg_repo.get_lasts_summary(),
            messages_count=self.msg_repo.get_total_messages_count(),
            user_input="",
        )

    def generate_summary(self, last_n_msgs: int) -> str:
        messages = self.msg_repo.get_last_n_messages(n=last_n_msgs)

        prompt = self.prompt_gen.summary(messages=messages)
        response = self.thinking_model(input_text=prompt, temp=1.0)

        self.msg_repo.add_summary(content=response)
        return response

    def process_history(self) -> List[str]:
        self.prompt_data.chat_history = self.msg_repo.get_last_n_messages(n=5)
        messages_count = self.msg_repo.get_total_messages_count()

        if messages_count % 10 == 0 and messages_count > 0:
            self.summary = self.generate_summary(last_n_msgs=10)

        return self.prompt_data.chat_history

    def generate_chat_prompt(self, top_3_movies: list[Movie]) -> str:

        self.msg_repo.add_message(role=RoleType.USER, content=self.prompt_data.user_input)
        self.summary_list = self.msg_repo.get_lasts_summary()

        pre_prompt = self.prompt_gen.movie_assistant(
            data=self.prompt_data, top_3_movies=top_3_movies
        )

        return pre_prompt

    def simple_model(self, input_text: str) -> str:
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=input_text,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )

        return response.text

    def thinking_model(self, input_text: str, temp: float = 2.0) -> str:
        if not input_text:
            raise ValueError("O prompt não pode ser vazio.")

        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=input_text,
            config=types.GenerateContentConfig(
                temperature=temp,
                thinking_config=types.ThinkingConfig(thinking_budget=-1),
                tools=[types.Tool(function_declarations=function_declarations())],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="AUTO",
                    )
                ),
            ),
        )

        fn = response.candidates[0].content.parts[0].function_call
        if fn:
           return self.function_call_response(fn)
        return response.candidates[0].content.parts[0].text

    def function_call_response(self, tool_call) -> str:
        if not tool_call:
            return ""

        if tool_call.name == "exit":
            self.exit_chat()
        if tool_call.name == "add_to_favorites":
            return self.user_movies.add_to_favorites(**tool_call.args)
        if tool_call.name == "set_rating":
            return self.user_movies.set_rating(**tool_call.args)
        if tool_call.name == "get_rating":
            return self.user_movies.get_rating(**tool_call.args)
        if tool_call.name == "set_watched":
            return self.user_movies.set_watched(**tool_call.args)
        if tool_call.name == "check_watched":
            watched = self.user_movies.check_watched(**tool_call.args)
            return (
                "Sim, você já assistiu a este filme."
                if watched
                else "Não, você ainda não assistiu a este filme."
            )
        if tool_call.name == "get_favorites":
            favorites = self.user_movies.get_favorites()
            return (
                f"Seus filmes favoritos têm os seguintes IDs: {', '.join(map(str, favorites))}"
                if favorites
                else "Você não tem filmes favoritos."
            )

    def exit_chat(self):
        print("Encerrando o chatbot. Até a próxima!")
        exit(0)
