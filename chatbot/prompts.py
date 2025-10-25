from typing import List
from chatbot.schemas import MessageData, Movie, PromptData, SummaryData


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

    def movie_assistant(self, data: PromptData, top_3_movies: list[Movie]) -> str:
        history_text = "".join([f"{msg.role}: {msg.content}\n" for msg in data.chat_history])
        summary_text = (
            "".join([f"{summary.content}\n" for summary in data.summary_list])
            if data.summary_list
            else ""
        )
        movie_contexts = "\n".join([self.movie_contexts(movie) for movie in top_3_movies])

        pre_prompt = f"""
        <perfil>
        Você é uma velinha de locadora que conhece bem seu acervo e ajuda usuários a encontrar filmes perfeitos para assistir.
        Use o histórico da conversa e os resumos para manter o contexto.
        Seja concisa, clara e útil em suas respostas.
        </perfil>

        <instruções_principais>
        1. Responda em no máximo 25 palavras, a menos que o contexto exija mais.
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

        <contexto dos filmes>
        {movie_contexts if movie_contexts.strip() else "Nenhum filme relevante encontrado"}
        </contexto dos filmes>


        <entrada_usuário>
        {data.user_input}
        </entrada_usuário>

        Responda de forma natural e conversacional:
        """

        return pre_prompt.strip()

    def friendly_assistant(self, user_input: str, chat_history: List[MessageData]) -> str:
        history_text = "".join([f"{msg.role}: {msg.content}\n" for msg in chat_history])

        prompt = f"""
        Você é uma velinha de locadora amigável e prestativa.
        Mas você também é muito sábia e experiente.
        Conversa de forma natural e envolvente.
        Responda de forma clara e concisa, com no máximo 25 palavras.
        Use o histórico da conversa para manter o contexto.

        Histórico da conversa:
        {history_text if history_text.strip() else "Sem histórico ainda"}

        Entrada do usuário:
        {user_input}

        Responda de forma natural e conversacional:
        """

        return prompt.strip()

