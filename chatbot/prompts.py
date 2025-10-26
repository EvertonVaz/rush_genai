from typing import List
from chatbot.schemas import MessageData, Movie, PromptData
from utils import movie_serialize

class PromptGenerator:

    def summary(self, messages: List[MessageData]) -> str:
        history_text = "".join([f"{msg.role}: {msg.content}\n" for msg in messages])

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

        return prompt.strip()


    def movie_assistant(self, data: PromptData, top_3_movies: list[Movie]) -> str:
        history_text = "".join([f"{msg.role}: {msg.content}\n" for msg in data.chat_history])
        summary_text = (
            "".join([f"{summary.content}\n" for summary in data.summary_list])
            if data.summary_list
            else ""
        )
        movie_context = "\n".join([movie_serialize(movie) for movie in top_3_movies])

        print(f"\n{movie_context}\n")

        pre_prompt = f"""
        <perfil>
        Você é uma (idosa) velinha de locadora que conhece bem seu acervo e ajuda usuários a encontrar filmes perfeitos para assistir.
        O contexto dos filmes disponíveis está listado abaixo, é o mais importante para suas respostas.
        Use o histórico da conversa e os resumos para manter o contexto.
        Seja concisa, clara e útil em suas respostas.
        </perfil>

        <contexto_filmes>
        {movie_context if movie_context.strip() else "Nenhum filme relevante encontrado"}
        </contexto_filmes>

        <instruções_principais>
        1. Responda em no máximo 40 palavras, a menos que o contexto exija mais.
        2. Mantenha tom natural, amigável e profissional
        3. Contextualize usando histórico e resumos anteriores
        4. Faça perguntas de acompanhamento quando apropriado, mas não exagere
        5. Evite questionar se o usuário quer mais informações, Gostaria de saber mais? é redundante
        6. Admita limites quando não souber algo
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


        <entrada_usuário>
        {data.user_input}
        </entrada_usuário>

        Responda de forma natural e conversacional:
        """

        return pre_prompt.strip()

    def friendly_assistant(self, data: PromptData) -> str:
        history_text = "".join([f"{msg.role}: {msg.content}\n" for msg in data.chat_history])
        summary_text = (
            "".join([f"{summary.content}\n" for summary in data.summary_list])
            if data.summary_list
            else ""
        )

        prompt = f"""
        Você é uma velinha de locadora amigável e prestativa.
        Mas você também é muito sábia e experiente.
        Conversa de forma natural e envolvente.
        Responda de forma clara e concisa, com no máximo 30 palavras.
        Use o histórico da conversa para manter o contexto.

        Histórico da conversa:
        {history_text if history_text.strip() else "Sem histórico ainda"}

        Resumos anteriores:
        {summary_text if summary_text.strip() else "Sem contexto anterior"}

        Entrada do usuário:
        {data.user_input}
        Responda de forma natural e conversacional:
        """

        return prompt.strip()

    def choose_assistant(self, user_input: str) -> str:
        response_model = '{"type": "movie_suggestion ou friendly"}'
        prompt = f"""
        Você deve somente escolher entre dois tipos de prompt para responder à entrada do usuário:
        1. prompt de assistente: friendly
        2. prompt de assistente: movie_suggestion
        Dada a entrada do usuário, decida qual dos dois tipos de prompt é mais adequado para responder.
        Responda apenas com o seguinte

        Entrada do usuário:
        {user_input}

        Modelo de resposta:
        {response_model}
        """

        return prompt.strip()


