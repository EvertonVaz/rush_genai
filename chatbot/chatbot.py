import json
from typing import List
from google import genai
from google.genai import types

from chatbot.database import UserRepository
from chatbot.schemas import ResponseData
from chatbot.func_declarations import function_declarations
from utils import favorite_serialize

from dotenv import load_dotenv


load_dotenv()


class PersistentChatbot:

    def simple_model(self, input_text: str) -> ResponseData:
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=input_text,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )

        try:
            response_dict = json.loads(response.text)

            if not isinstance(response_dict, dict):
                raise ValueError(f"Esperava dict, recebeu {type(response_dict)}")

            return ResponseData(**response_dict)
        
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}, resposta recebida: {response.text}")
        except TypeError as e:
            print(f"Erro de tipo: {e}, resposta recebida: {response.text}")

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
        user_movies = UserRepository()

        if tool_call.name == "exit":
            self.exit_chat()
        if tool_call.name == "add_to_favorites":
            return user_movies.add_to_favorites(**tool_call.args)
        if tool_call.name == "set_rating":
            return user_movies.set_rating(**tool_call.args)
        if tool_call.name == "get_rating":
            return user_movies.get_rating(**tool_call.args)
        if tool_call.name == "set_watched":
            return user_movies.set_watched(**tool_call.args)
        if tool_call.name == "check_watched":
            watched = user_movies.check_watched(**tool_call.args)
            return (
                "Sim, você já assistiu a este filme."
                if watched
                else "Não, você ainda não assistiu a este filme."
            )
        if tool_call.name == "get_favorites":
            favorites = user_movies.get_favorites()
            return (
                f"Seus filmes favoritos:\n{'\n'.join(map(favorite_serialize, favorites))}"
                if favorites
                else "Você não tem filmes favoritos."
            )

    def exit_chat(self):
        print("Encerrando o chatbot. Até a próxima!")
        exit(0)
