from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatbot.models import Message, Base, Summary, Favorites
from chatbot.schemas import MessageData, SummaryData, UserMovieData

DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MessageRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session if db_session else next(get_db())

    def add_message(self, role: str, content: str) -> Message:
        message = Message(role=role, content=content)
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def add_summary(self, content: str) -> Summary:
        summary = Summary(content=content)
        self.db_session.add(summary)
        self.db_session.commit()
        self.db_session.refresh(summary)
        return summary

    def get_recent_messages(self, n: int) -> List[MessageData]:
        messages = (
            self.db_session.query(Message)
            .order_by(Message.created_at.desc())
            .limit(n)
            .all()
        )

        result = []
        for msg in messages:
            result.append(MessageData(role=msg.role, content=msg.content))
        return result[::-1]

    def get_total_messages_count(self) -> int:
        count = self.db_session.query(Message).count()
        return count

    def get_lasts_summary(self) -> List[SummaryData]:
        summarys = (
            self.db_session.query(Summary)
            .order_by(Summary.created_at.desc())
            .limit(10)
            .all()
        )
        result = []
        for summary in summarys:
            result.append(SummaryData(content=summary.content))
        return result[::-1]


class UserRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session if db_session else next(get_db())

    def get_favorites(self) -> List[UserMovieData]:
        # Retorna lista de IDs dos filmes favoritos
        favorites = self.db_session.query(Favorites).filter(Favorites.is_favorite == True).all()
        favorites = []
        for movie in favorites:
            favorites.append(UserMovieData(
                filme_id=movie.filme_id,
                titulo=movie.titulo,
                rating=movie.rating,
                is_favorite=movie.is_favorite,
                watching=movie.watching
            ))
        return favorites

    def add_to_favorites(self, movie_id: str, titulo: str) -> str:
        # Adiciona filme aos favoritos
        favorites = Favorites(filme_id=movie_id, titulo=titulo, is_favorite=True)
        existing = (
            self.db_session.query(Favorites)
            .filter(Favorites.filme_id == movie_id)
            .first()
        )
        if existing:
            return f"Filme {titulo} já está nos favoritos."
        self.db_session.add(favorites)
        self.db_session.commit()
        self.db_session.refresh(favorites)
        return f"Filme {titulo} adicionado aos favoritos."

    def get_rating(self, movie_id: str) -> str:
        # Retorna a nota do usuário para o filme
        favorites = self.db_session.query(Favorites).filter(Favorites.filme_id == movie_id).first()
        if favorites:
            return f"O filme {favorites.titulo} tem nota {favorites.rating}."
        return "Filme não encontrado."

    def set_rating(self, movie_id: str, rating: int) -> str:
        # Define uma nota para o filme
        favorites = self.db_session.query(Favorites).filter(Favorites.filme_id == movie_id).first()
        if favorites:
            favorites.rating = rating
            self.db_session.commit()
            self.db_session.refresh(favorites)
            return "Nota atualizada com sucesso."
        return "Filme não encontrado."

    def check_watched(self, movie_id: str) -> bool:
        # Verifica se o filme foi assistido
        favorites = self.db_session.query(Favorites).filter(Favorites.filme_id == movie_id).first()
        if favorites:
            return favorites.watching
        return False

    def set_watched(self, movie_id: str) -> str:
        # Marca um filme como assistido
        favorites = self.db_session.query(Favorites).filter(Favorites.filme_id == movie_id).first()
        if favorites:
            favorites.watching = True
            self.db_session.commit()
            self.db_session.refresh(favorites)
            return f"Filme '{favorites.titulo}' marcado como assistido."
        return "Filme não encontrado."
