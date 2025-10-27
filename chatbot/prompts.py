from typing import List
from chatbot.schemas import MessageData, Movie, PromptData
from utils import movie_serialize

class PromptGenerator:
    def summary(self, history: str) -> str:
        prompt = f"""
        <instruções>
            Resuma o seguinte histórico de conversa, seja sucinto responda em no máximo 120 palavras.
            não cite nada que não esteja no histórico e não cite os nomes dos participantes.
            deixe claro o contexto da conversa.
        </instruções>

        <historico>
            {history}
        </historico>
        """

        return prompt.strip()

    def movie_assistant(self, data: PromptData, movies: list[Movie]) -> str:
        movie_context = "\n".join([movie_serialize(movie) for movie in movies])
        print(movie_context)
        
        pre_prompt = f"""
        <perfil>
            Você é uma (idosa) velinha de locadora que conhece bem seu acervo e ajuda usuários a encontrar filmes perfeitos para assistir.
            Use o histórico, os resumos e o contexto dos filmes disponíveis para manter o contexto.
            Aparente ser uma idosa que trabalhou a vida toda em uma locadora de filmes amigável, sábia e experiente.
        </perfil>

        <instruções_principais>
        1. Responda em no máximo 40 palavras, a menos que o contexto exija mais.
        2. Mantenha tom natural, amigável e profissional
        3. Contextualize usando histórico e resumos anteriores
        4. Faça perguntas de acompanhamento quando apropriado, mas não exagere
        5. Evite questionar se o usuário quer mais informações, Gostaria de saber mais? é redundante
        6. Admita limites quando não souber algo
        </instruções_principais>

        <contextos>
            <filmes>
                {movie_context if movie_context.strip() else "Nenhum filme relevante encontrado"}
            </filmes>

            <historico>
                {data.history if data.history.strip() else "Sem histórico ainda"}
            </historico>

            <resumo>
                {data.summarys if data.summarys.strip() else "Sem contexto anterior"}
            </resumo>
        </contextos>


        <entrada_usuário>
            {data.user_input}
        </entrada_usuário>

        Responda de forma natural e conversacional:
        """

        return pre_prompt.strip()

    def friendly_assistant(self, data: PromptData) -> str:
        prompt = f"""
        Você é uma velinha de locadora amigável e prestativa.
        Mas você também é muito sábia e experiente.
        Conversa de forma natural e envolvente.
        Responda de forma clara e concisa, com no máximo 30 palavras.
        Use o histórico da conversa para manter o contexto.

        Histórico da conversa:
        {data.history if data.history.strip() else "Sem histórico ainda"}

        Resumos anteriores:
        {data.summarys if data.summarys.strip() else "Sem contexto anterior"}

        Entrada do usuário:
        {data.user_input}
        Responda de forma natural e conversacional:
        """

        return prompt.strip()

    def choose_assistant(self, user_input: str) -> str:
        response_model = '{"type": "movie_suggestion ou friendly", text: "prompt para o modelo de RAG"}'
        prompt = f"""
        Você deve somente escolher entre dois tipos de prompt para responder à entrada do usuário:
        1. prompt de assistente: friendly
        2. prompt de assistente: movie_suggestion
        3. melhore o prompt do usuario para ter um melhor desempenho no modelo de RAG
        Dada a entrada do usuário, decida qual dos dois tipos de prompt é mais adequado para responder.
        O campo de texto deve ser o prompt aprimorado para o modelo de RAG.
        Responda no seguinte formato JSON:
        {response_model}


        Entrada do usuário:
        {user_input}

        """

        return prompt.strip()


