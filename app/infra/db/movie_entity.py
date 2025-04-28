from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infra.db.session import BASE

class MovieDB(BASE):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"))

    studio = relationship("StudioDB", backref="movies")
    producers = relationship(
        "ProducerDB",
        secondary="movie_x_producers",
        back_populates="movies"
    )
