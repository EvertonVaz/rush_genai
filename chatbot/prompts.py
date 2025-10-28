from typing import List
from chatbot.schemas import MessageData, Movie, PromptData
from utils import movie_serialize

class PromptGenerator:
    def summary(self, history: str) -> str:
        return f"Resuma em max 120 palavras, sem citar nomes:\n{history}"

    def movie_assistant(self, data: PromptData, movies: list[Movie]) -> str:
        movie_context = "\n".join([movie_serialize(movie) for movie in movies])

        prompt = f"""seja sábia e experiente. Max 60 palavras, tom natural.

        Filmes: {movie_context or "Nenhum"}
        Histórico: {data.history or "Vazio"}
        Resumo: {data.summarys or "Vazio"}
        Usuario: {data.user_input}"""

        return prompt.strip()


    def friendly_assistant(self, data: PromptData) -> str:
        prompt = f"""seja amigável e sábia. Max 60 palavras.

        Histórico: {data.history or "Vazio"}
        Resumo: {data.summarys or "Vazio"}
        Usuario: {data.user_input}"""

        return prompt.strip()


    def choose_assistant(self, data: PromptData) -> str:
        prompt = f"""Roteador: escolha movie_suggestion (recomendações/detalhes/ações com filmes) ou friendly (saudação/chat casual).

        IMPORTANTE: Analise histórico para resolver "ela"/"esse filme". Ações em filmes = movie_suggestion.
        Campo "text": otimize para RAG, incluindo título do histórico se houver.

        Exemplos:
        "filme de animação" → {{"type":"movie_suggestion","text":"filme animação anime"}}
        "adicione ela" (histórico: *nome do filme*) → {{"type":"movie_suggestion","text":"*nome do filme*: adicionar aos favoritos"}}
        "conte mais sobre ele" (histórico: *nome do filme*) → {{"type":"movie_suggestion","text":"*nome do filme*: adicionar aos favoritos"}}
        "qual a avaliação dele" (histórico: *nome do filme*) → {{"type":"movie_suggestion","text":"*nome do filme*: avaliação"}}
        "oi" → {{"type":"friendly","text":"oi, tudo bem?"}}

        Histórico: {data.history or "Vazio"}
        Usuario: {data.user_input}

        JSON apenas: {{"type":"...","text":"..."}}"""

        return prompt.strip()



