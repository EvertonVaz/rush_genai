from typing import List
from chatbot.prompts import PromptGenerator
from chatbot.chatbot import ChatBot
from chatbot.database import MessageRepository
from chatbot.history_manager import HistoryManager
from chatbot.schemas import Movie, ResponseType, RoleType, PromptData
from process_json import ProcessJSON
import streamlit as st

st.set_page_config(
    page_title="🎬 Locadora",
    page_icon="👵",
    layout="wide",
)

def main():
    st.title("Locadora 👵")
    st.write("Tenha paciência comigo, ainda estou em desenvolvimento!")

    prompt_type = PromptGenerator()
    chat = ChatBot()
    msg_repo = MessageRepository()
    history = HistoryManager()
    process = ProcessJSON()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    messages = st.container(height=300)
    for msg in st.session_state.messages:
        with messages.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Say something"):
        with messages.chat_message("user"):
            st.write(user_input)
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            prompt_data = history.update_prompt_data(user_input=user_input)

        with st.spinner("🤔 Pensando..."):
            pre_prompt = prompt_type.choose_assistant(prompt_data)
            response = chat.simple_model(pre_prompt)

            if response.type == ResponseType.FRIENDLY:
                print(f"\033[33mFriendly response selected\033[0m\n{prompt_data.user_input}")
                pre_prompt = prompt_type.friendly_assistant(prompt_data)
                response = chat.thinking_model(input_text=pre_prompt)
            elif response.type == ResponseType.MOVIE_SUGGESTION:
                print(f"\033[34mMovie suggestion response selected\033[0m\n{prompt_data.user_input}")
                movies = process.similiar_movies(response.text)
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

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })


if __name__ == "__main__":
    main()

