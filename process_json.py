import json
import chromadb
from chatbot.schemas import Movie
from chromadb import Collection

class ProcessJSON:

    def __init__(self, movies_file_path: str = "movies.json"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.movies_file_path = movies_file_path
        self._setup_collection()

    def _setup_collection(self):
        if "movies" in [col.name for col in self.client.list_collections()]:
            self.movies_collection = self.client.get_collection(name="movies")
        else:
            self.movies_collection = self.client.create_collection(name="movies")


    def _get_int(self, value:str) -> int:
        if(value.isdigit()):
            return int(value)
        return 0

    def read_file(self) -> list[Movie]:
        result = []
        with open(self.movies_file_path, "r", encoding="utf-8") as file:
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
                    avaliacao=float(movie.get("avaliacao", 0.0)) if movie.get("avaliacao", "0.0") != '' else 0.0,
                    numVotos=self._get_int(movie.get("numVotos", 0)),
                    generos=movie.get("generos", []),
                    elenco=movie.get("elenco", []),
                    url_imagem=movie.get("url_imagem", "")
                )
                result.append(movie_obj)

        return result

    def generate_metadata(self, collection: Collection, movies: list[Movie]):
        print("Generating metadata...")
        ids = [movie.imdb_id if getattr(movie, "imdb_id", "") else f"movie_{i}" for i, movie in enumerate(movies)]
        documents = [ (movie.titulo) for movie in movies ]
        metadatas = [movie.model_dump() for movie in movies]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
