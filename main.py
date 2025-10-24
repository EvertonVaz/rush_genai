from chatbot.chatbot import PersistentChatbot
from chatbot.schemas import Movie
from process_json import ProcessJSON
import streamlit as st

def main():
    st.title("Velinha da locadora 👵")
    st.write("Tenha paciência comigo, ainda estou em desenvolvimento!")

    process = ProcessJSON()

    messages = st.container(height=500)
    if user_input := st.chat_input("Say something"):
        with messages.chat_message("user"):
            st.write(user_input)

        get_query = process.movies_collection.query(
            query_texts=[user_input],
            n_results=3
        )

        top_3_movies = []
        for movie_data in get_query["metadatas"]:
            for data in movie_data:
                top_3_movies.append(Movie(**data))

        if response := PersistentChatbot.chatbot(user_input, top_3_movies):
            with messages.chat_message("assistant"):
                st.write(response)


if __name__ == "__main__":
    main()