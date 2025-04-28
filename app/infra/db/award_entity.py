from sqlalchemy import Column, Integer, String, ForeignKey
from app.infra.db.session import BASE

class AwardDB(BASE):
    __tablename__ = "awards"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    year = Column(Integer, nullable=False)
    winner = Column(String, nullable=True)
