from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infra.db.session import BASE


class ProducerDB(BASE):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    movies = relationship(
        "MovieDB",
        secondary="movie_x_producers",
        back_populates="producers"
    )
