from enum import Enum
from pydantic import BaseModel
from typing import Optional

class RoleType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageData(BaseModel):
    role: RoleType
    content: str

class SummaryData(BaseModel):
    content: str

class PromptData(BaseModel):
    chat_history: list[MessageData]
    summary_list: list[SummaryData]
    messages_count: int
    user_input: str


class Movie(BaseModel):
    imdb_id: str
    titulo: str
    rank: str
    certificado: str
    ano_inicio: int
    ano_fim: int
    episodios: int
    duracao: int
    tipo: str
    pais_origem: str
    idioma: str
    sinopse: str
    avaliacao: float
    numVotos: int
    generos: str
    elenco: str
    url_imagem: str