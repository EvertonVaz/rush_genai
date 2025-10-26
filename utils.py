from chatbot.schemas import Movie



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
