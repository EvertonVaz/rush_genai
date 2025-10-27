from time import time
from chatbot.schemas import Movie, UserMovieData

def movie_serialize(movie: Movie) -> str:
    return f"""
    ID: {movie.imdb_id}
    Título: {movie.titulo}
    Elenco: {movie.elenco}
    Gêneros: {movie.generos}
    Sinopse: {movie.sinopse}
    Avaliação: {movie.avaliacao} ({movie.numVotos} votos)
    País de origem: {movie.pais_origem}
    Idioma: {movie.idioma}
    Tipo: {movie.tipo}
    Episódios: {movie.episodios}
    Ano Lançamento: {movie.ano_inicio}
    Ano Término: {movie.ano_fim}
    Duração: {movie.duracao} minutos

    """

def favorite_serialize(movie: UserMovieData) -> str:
    return f"""
    ID: {movie.filme_id}
    Título: {movie.titulo}
    Assistido?: {'Sim' if movie.watching else 'Não'}
    Nota do usuário: {movie.rating if movie.rating else 'Sem nota'}
    """

def measure_time_execution(function):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = function(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        print(f"⏱️ {function.__name__} levou {execution_time:.2f}s para executar")
        return result
    return wrapper