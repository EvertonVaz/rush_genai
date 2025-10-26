from typing import List
from chatbot.prompts import PromptGenerator
from chatbot.chatbot import PersistentChatbot
from chatbot.database import MessageRepository
from chatbot.history_manager import HistoryManager
from chatbot.schemas import Movie, ResponseType, RoleType, PromptData
from process_json import ProcessJSON
import streamlit as st


def similiar_movies(user_input: str) -> List[Movie]:
    process = ProcessJSON()

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
    msg_repo = MessageRepository()
    history = HistoryManager()

    messages = st.container(height=200)
    if user_input := st.chat_input("Say something"):
        with messages.chat_message("user"):
            st.write(user_input)

            prompt_data = history.update_prompt_data(user_input=user_input)

        pre_prompt = prompt_type.choose_assistant(prompt_data.user_input)
        response = chat.simple_model(pre_prompt)

        if response.type == ResponseType.FRIENDLY:
            print(f"\033[33mFriendly response selected\033[0m\n{prompt_data.user_input}")
            pre_prompt = prompt_type.friendly_assistant(prompt_data)
            response = chat.thinking_model(input_text=pre_prompt)
        elif response.type == ResponseType.MOVIE_SUGGESTION:
            print(f"\033[34mMovie suggestion response selected\033[0m\n{prompt_data.user_input}")
            movies = similiar_movies(response.text)
            pre_prompt = prompt_type.movie_assistant(prompt_data, movies)
            response = chat.thinking_model(input_text=pre_prompt)

        with messages.chat_message("assistant"):
            st.write(response)
            if (prompt_data.messages_count) % 10 == 0 and prompt_data.messages_count > 0:
                pre_prompt = prompt_type.summary(history.get_chat_history(10))
                summary_response = chat.thinking_model(pre_prompt)
                msg_repo.add_summary(content=summary_response)
            msg_repo.add_message(role=RoleType.USER, content=user_input)
            msg_repo.add_message(role=RoleType.ASSISTANT, content=response)






if __name__ == "__main__":
    main()

