import json
from typing import List
from google import genai
from google.genai import types

from chatbot.database import UserRepository
from chatbot.schemas import ResponseData
from chatbot.func_declarations import function_declarations
from utils import favorite_serialize, measure_time_execution

from dotenv import load_dotenv


load_dotenv()


class ChatBot:

    def _clean_str(self, texto: str) -> str:
        """Remove markdown code blocks da resposta"""
        texto = texto.strip()

        if texto.startswith("```json"):
            texto = texto[7:]
        elif texto.startswith("```"):
            texto = texto[3:]
        if texto.endswith("```"):
            texto = texto[:-3]

        return texto.strip()

    @measure_time_execution
    def simple_model(self, input_text: str) -> ResponseData:
        if not input_text:
            raise ValueError("O prompt não pode ser vazio.")

        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=input_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )

        try:
            response = self._clean_str(response.text)
            response_dict = json.loads(response)

            if not isinstance(response_dict, dict):
                raise ValueError(f"Esperava dict, recebeu {type(response_dict)}, {response}")

            return ResponseData.model_validate(response_dict)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}, resposta recebida: {response.text}")
        except TypeError as e:
            print(f"Erro de tipo: {e}, resposta recebida: {response.text}")

    @measure_time_execution
    def thinking_model(self, input_text: str, temp: float = 1.0) -> str:
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
