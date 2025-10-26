import json
from typing import List
from chatbot.prompts import PromptGenerator
from chatbot.chatbot import PersistentChatbot
from chatbot.schemas import Movie, ResponseData, ResponseType
from process_json import EmbeddingTextFunction, ProcessJSON
import streamlit as st


def similiar_movies(user_input: str) -> List[Movie]:
    embedding = EmbeddingTextFunction()
    process = ProcessJSON()

    # escaped_passage = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    get_query = process.movies_collection.query(
        query_texts=[user_input],
        n_results=3
    )

    similiar_movies = []
    for movie_data in get_query["metadatas"]:
        for data in movie_data:
            similiar_movies.append(Movie(**data))

    return similiar_movies

def main():
    st.title("Velinha da locadora 👵")
    st.write("Tenha paciência comigo, ainda estou em desenvolvimento!")

    prompt_type = PromptGenerator()
    chat = PersistentChatbot()

    messages = st.container(height=200)
    if user_input := st.chat_input("Say something"):
        with messages.chat_message("user"):
            st.write(user_input)

            chat.prompt_data.user_input = user_input

        pre_prompt = prompt_type.choose_assistant(chat.prompt_data.user_input)
        response = chat.simple_model(pre_prompt)
        response = ResponseData(**json.loads(chat.simple_model(pre_prompt)))

        if response.type == ResponseType.FRIENDLY:
            print("Friendly response selected")
            pre_prompt = prompt_type.friendly_assistant(chat.prompt_data)
            response = chat.thinking_model(input_text=pre_prompt)
        elif response.type == ResponseType.MOVIE_SUGGESTION:
            print("Movie suggestion response selected")
            movies = similiar_movies(chat.prompt_data.user_input)
            pre_prompt = prompt_type.movie_assistant(chat.prompt_data, movies)
            response = chat.thinking_model(input_text=pre_prompt)

        with messages.chat_message("assistant"):
            st.write(response)






if __name__ == "__main__":
    # main()
    from sys import argv

    prompt = " ".join(argv[1:])
    sm = similiar_movies(prompt)
    print(prompt)
    for movie in sm:
        print(f"""
Titulo: {movie.titulo}
Sinopse: {movie.sinopse}
Elenco: {movie.elenco}
Generos: {movie.generos}
Avaliação: {movie.avaliacao}
""".strip())
        print(13*"---")
