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