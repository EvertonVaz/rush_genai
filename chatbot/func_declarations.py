def function_declarations() -> list[dict]:
    functions = [
        {
            "name": "exit",
            "description": "Encerrar a conversa do chatbot.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        },
        {
            "name": "get_favorites",
            "description": "Obter a lista de filmes favoritos do usuário.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        },
        {
            "name": "add_to_favorites",
            "description": "Adicionar um filme aos favoritos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_id": {
                        "type": "string",
                        "description": "ID do filme a ser adicionado aos favoritos."
                    },
                    "titulo": {
                        "type": "string",
                        "description": "Título do filme a ser adicionado aos favoritos."
                    }
                },
                "required": ["movie_id", "titulo"],
            }
        },
        {
            "name": "set_rating",
            "description": "Definir uma nota para um filme.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_id": {
                        "type": "string",
                        "description": "ID do filme a ser avaliado."
                    },
                    "rating": {
                        "type": "integer",
                        "description": "Nota a ser atribuída ao filme (0-10)."
                    }
                },
                "required": ["movie_id", "rating"],
            }
        },
        {
            "name": "get_rating",
            "description": "Obter a nota do usuário para um filme.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_id": {
                        "type": "string",
                        "description": "ID do filme cuja nota será recuperada."
                    }
                },
                "required": ["movie_id"],
            }
        },
        {
            "name": "set_watched",
            "description": "Marcar um filme como assistido.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_id": {
                        "type": "string",
                        "description": "ID do filme a ser marcado como assistido."
                    }
                },
                "required": ["movie_id"],
            }
        },
        {
            "name": "check_watched",
            "description": "Verificar se um filme foi assistido.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_id": {
                        "type": "string",
                        "description": "ID do filme a ser verificado."
                    }
                },
                "required": ["movie_id"],
            }
        }
    ]
    return functions
