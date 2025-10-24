from chatbot.chatbot import PersistentChatbot
from chatbot.schemas import Movie
from process_json import ProcessJSON

def main():

    process = ProcessJSON()
    # movies = process.read_file()
    # process.generate_metadata(process.movies_collection, movies)

    while True:
        user_input = input("Q: ")

        if user_input.lower() == 'bye':
            break

        get_query = process.movies_collection.query(
            query_texts=[user_input],
            n_results=3
        )

        top_3_movies = []
        for movie_data in get_query["metadatas"]:
            for data in movie_data:
                top_3_movies.append(Movie(**data))


        PersistentChatbot.chatbot(user_input, top_3_movies)



if __name__ == "__main__":
    main()