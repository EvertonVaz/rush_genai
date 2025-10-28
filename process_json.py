import json
from typing import List
import chromadb
from chatbot.schemas import Movie
from chromadb import Collection, EmbeddingFunction, Embeddings, Documents
from sentence_transformers import SentenceTransformer
from utils import measure_time_execution, movie_serialize


class EmbeddingTextFunction(EmbeddingFunction):
    _model_cache = None

    def __init__(self):
        if EmbeddingTextFunction._model_cache is None:
            EmbeddingTextFunction._model_cache = SentenceTransformer(
                "paraphrase-multilingual-MiniLM-L12-v2"
            )
        self._embedding_model = EmbeddingTextFunction._model_cache

    def __call__(self, input: Documents) -> Embeddings:
        return self._embedding_model.encode(input)



class ProcessJSON:

    def __init__(self, movies_file_path: str = "/usr/src/rush_genai/movies.json"):
        self._client = chromadb.PersistentClient(
            path="./chroma_db", settings=chromadb.Settings(anonymized_telemetry=False)
        )
        self._movies_file_path = movies_file_path
        self._setup_collection()

    def _setup_collection(self):
        self._movies_collection = self._client.get_or_create_collection(
            name="movies", embedding_function=EmbeddingTextFunction()
        )

        if self._movies_collection.count() == 0:
            self._generate_metadata(self._movies_collection, self.read_file())

    @property
    def movies_collection(self):
        """Propriedade pública para acessar a collection"""
        return self._movies_collection

    def _get_int(self, value: str) -> int:
        if value.isdigit():
            return int(value)
        return 0

    def read_file(self) -> list[Movie]:
        result = []
        with open(self._movies_file_path, "r", encoding="utf-8") as file:
            movies_data = json.load(file)
            for movie in movies_data:
                movie_obj = Movie(
                    imdb_id=movie.get("imdb_id", ""),
                    titulo=movie.get("titulo", ""),
                    rank=movie.get("rank", ""),
                    certificado=movie.get("certificado", ""),
                    ano_inicio=self._get_int(movie.get("ano_inicio", 0)),
                    ano_fim=self._get_int(movie.get("ano_fim", 0)),
                    episodios=self._get_int(movie.get("episodios", 0)),
                    duracao=self._get_int(movie.get("duracao", 0)),
                    tipo=movie.get("tipo", ""),
                    pais_origem=movie.get("pais_origem", ""),
                    idioma=movie.get("idioma", ""),
                    sinopse=movie.get("sinopse", ""),
                    avaliacao=(
                        float(movie.get("avaliacao", 0.0))
                        if movie.get("avaliacao", "0.0") != ""
                        else 0.0
                    ),
                    numVotos=self._get_int(movie.get("numVotos", 0)),
                    generos=movie.get("generos", []),
                    elenco=movie.get("elenco", []),
                    url_imagem=movie.get("url_imagem", ""),
                )
                result.append(movie_obj)

        return result

    def _generate_metadata(
        self, collection: Collection, movies: list[Movie], limit: int = None
    ):
        print("Generating metadata...")
        if limit:
            movies = movies[:limit]
        ids = [
            movie.imdb_id if getattr(movie, "imdb_id", "") else f"movie_{i}"
            for i, movie in enumerate(movies)
        ]
        documents = [movie_serialize(movie) for movie in movies]
        metadatas = [movie.model_dump() for movie in movies]

        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        print(f"✅ {len(movies)} filmes adicionados com sucesso!")

    @measure_time_execution
    def similiar_movies(self, user_input: str) -> List[Movie]:

        get_query = self._movies_collection.query(
            query_texts=[user_input],
            n_results=3
        )

        similiar_movies = []
        for movie_data in get_query["metadatas"]:
            for data in movie_data:
                similiar_movies.append(Movie(**data))

        return similiar_movies


if __name__ == "__main__":
    pass
