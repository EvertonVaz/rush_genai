from typing import List
from google import genai
from google.genai import types
from chatbot.database import MessageRepository, UserRepository
from chatbot.schemas import PromptData, RoleType

from dotenv import load_dotenv

from chatbot.schemas import Movie

load_dotenv()

class PersistentChatbot:

    def __init__(self):
        self.repo = MessageRepository()
        self.user_movies = UserRepository()
        self.prompt = PromptData(
            chat_history=self.repo.get_last_n_messages(n=5),
            summary_list=self.repo.get_lasts_summary(),
            messages_count=self.repo.get_total_messages_count(),
            user_input=""
        )

    def generate_summary(self, last_n_msgs: int) -> str:
        messages = self.repo.get_last_n_messages(n=last_n_msgs)

        history_text = ''.join([f"{msg.role}: {msg.content}\n" for msg in messages[::-1]])

        prompt = f"""
        <instruções>
            Resuma o seguinte histórico de conversa, seja sucinto responda em no máximo 120 palavras.
            não cite nada que não esteja no histórico e não cite os nomes dos participantes.
            deixe claro o contexto da conversa.
        </instruções>

        <historico>
            {history_text}
        </historico>
        """

        response = self.generate_llm_response(input_text=prompt, temp=1.0)

        self.repo.add_summary(content=response)
        return response


    def process_history(self) -> List[str]:
        self.prompt.chat_history = self.repo.get_last_n_messages(n=5)
        messages_count = self.repo.get_total_messages_count()

        if messages_count % 10 == 0 and messages_count > 0:
            self.summary = self.generate_summary(last_n_msgs=10)

        return self.prompt.chat_history

    def movie_contexts(self, movie: Movie) -> str:
        movie_contexts = f"ID: {movie.imdb_id}\n"
        movie_contexts += f"Título: {movie.titulo}\n"
        movie_contexts += f"Ano Lançamento: {movie.ano_inicio}\n"
        movie_contexts += f"Ano Término: {movie.ano_fim}\n"
        movie_contexts += f"Gêneros: {movie.generos}\n"
        movie_contexts += f"Sinopse: {movie.sinopse}\n"
        movie_contexts += f"Avaliação: {movie.avaliacao}\n"
        movie_contexts += f"Elenco: {movie.elenco}\n"
        movie_contexts += f"Episodios: {movie.episodios}\n"
        movie_contexts += f"Duração: {movie.duracao} minutos\n"
        movie_contexts += f"País de origem: {movie.pais_origem}\n"
        movie_contexts += f"Idioma: {movie.idioma}\n"
        movie_contexts += f"Tipo: {movie.tipo}\n"

        return movie_contexts

    def generate_chat_prompt(self, is_new_chat: bool, top_3_movies: list[Movie]) -> str:

        self.repo.add_message(role="user", content=self.prompt.user_input)
        self.summary_list = self.repo.get_lasts_summary()
        summarys = self.summary_list

        history_text = ''.join([f"{msg.role}: {msg.content}\n" for msg in self.prompt.chat_history])
        summary_text = ''.join([f"{summary.content}\n" for summary in summarys]) if summarys else ''
        movie_contexts = '\n'.join([self.movie_contexts(movie) for movie in top_3_movies])

        pre_prompt = f"""
        <perfil>
        Você é um crítico de cinema experiente, pimpão e bondoso, e vai responder ao usuário com base no banco de dados de filmes fornecido.
        Use o histórico da conversa e os resumos para manter o contexto.
        Seja conciso, claro e útil em suas respostas.
        </perfil>

        <instruções_principais>
        1. Responda em no máximo 25 palavras, a menos que o contexto exija mais.
        2. Mantenha tom natural, amigável e profissional
        3. Contextualize usando histórico e resumos anteriores
        4. Faça perguntas de acompanhamento quando apropriado
        5. Admita limites quando não souber algo
        {"6. NOVA CONVERSA: Ignore resumos e histórico, responda conforme contexto" if is_new_chat else "6. Aproveite o contexto anterior para continuidade temática"}
        7. Evite questionar se o usuário quer mais informações, Gostaria de saber mais? é redundante
        </instruções_principais>

        <funções_disponíveis>
        exit(): Encerra a conversa do chatbot.
        get_favorites(): Obtém a lista de filmes favoritos do usuário.
        add_to_favorites(movie_id: str): Adiciona um filme aos favoritos.
        set_rating(movie_id: str, rating: int): Define uma nota para um filme.
        get_rating(movie_id: str): Obtém a nota do usuário para um filme.
        set_watched(movie_id: str): Marca um filme como assistido.
        check_watched(movie_id: str): Verifica se um filme foi assistido.
        </funções_disponíveis>

        <histórico_recente>
        {history_text if history_text.strip() else "Sem histórico ainda"}
        </histórico_recente>

        <resumo_contexto>
        {summary_text if summary_text.strip() else "Sem contexto anterior"}
        </resumo_contexto>

        <contexto dos filmes>
        {movie_contexts if movie_contexts.strip() else "Nenhum filme relevante encontrado"}
        </contexto dos filmes>


        <entrada_usuário>
        {self.prompt.user_input}
        </entrada_usuário>

        Responda de forma natural e conversacional:
        """

        return pre_prompt

    def function_declarations(self) -> list[dict]:
        result = [
            {
                "name": "exit",
                "description": "Encerrar a conversa do chatbot.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            },
            {
                "name": "get_favorites",
                "description": "Obter a lista de filmes favoritos do usuário.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            },
            {
                "name": "add_to_favorites",
                "description": "Adicionar um filme aos favoritos.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_id": {
                            "type": "string",
                            "description": "ID do filme a ser adicionado aos favoritos."
                        },
                        "titulo": {
                            "type": "string",
                            "description": "Título do filme a ser adicionado aos favoritos."
                        }
                    },
                    "required": ["movie_id", "titulo"],
                }
            },
            {
                "name": "set_rating",
                "description": "Definir uma nota para um filme.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_id": {
                            "type": "string",
                            "description": "ID do filme a ser avaliado."
                        },
                        "rating": {
                            "type": "integer",
                            "description": "Nota a ser atribuída ao filme (0-10)."
                        }
                    },
                    "required": ["movie_id", "rating"],
                }
            },
            {
                "name": "get_rating",
                "description": "Obter a nota do usuário para um filme.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_id": {
                            "type": "string",
                            "description": "ID do filme cuja nota será recuperada."
                        }
                    },
                    "required": ["movie_id"],
                }
            },
            {
                "name": "set_watched",
                "description": "Marcar um filme como assistido.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_id": {
                            "type": "string",
                            "description": "ID do filme a ser marcado como assistido."
                        }
                    },
                    "required": ["movie_id"],
                }
            },
            {
                "name": "check_watched",
                "description": "Verificar se um filme foi assistido.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_id": {
                            "type": "string",
                            "description": "ID do filme a ser verificado."
                        }
                    },
                    "required": ["movie_id"],
                }
            }
        ]
        return result

    def generate_llm_response(self, input_text: str, temp: float = 2.0) -> str:
        if not input_text:
            raise ValueError("O prompt não pode ser vazio.")

        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=input_text,
            config=types.GenerateContentConfig(
                temperature=temp,
                thinking_config=types.ThinkingConfig(thinking_budget=-1),
                tools=[types.Tool(function_declarations=self.function_declarations())],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="AUTO",
                    )
                ),
            )
        )
        if response.candidates[0].content.parts[0].function_call:
            tool_call = response.candidates[0].content.parts[0].function_call
            print(tool_call)
            if tool_call.name == "exit":
                self.exit_chat()
            if tool_call.name == "get_favorites":
                favorite_ids = self.user_movies.get_favorites()
                return f"Seus filmes favoritos têm os seguintes IDs: {', '.join(map(str, favorite_ids))}" if favorite_ids else "Você não tem filmes favoritos."
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
                return "Sim, você já assistiu a este filme." if watched else "Não, você ainda não assistiu a este filme."

        return response.text

    @staticmethod
    def chatbot(user_input, top_3_movies: list[Movie] = []):
        chat = PersistentChatbot()
        is_new_chat = True
        try:
            chat.prompt.user_input = user_input

            prompt = chat.generate_chat_prompt(is_new_chat, top_3_movies)
            response = chat.generate_llm_response(prompt)
            print(f"A: {response}\n")

            chat.repo.add_message(role=RoleType.ASSISTANT, content=response)
            chat.process_history()
            is_new_chat = False
        except ValueError as e:
            print(f"Error: {e}\n")

    def exit_chat(self):
        print("Encerrando o chatbot. Até a próxima!")
        exit(0)


if __name__ == "__main__":
    PersistentChatbot.chatbot()