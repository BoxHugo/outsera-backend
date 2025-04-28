from sqlalchemy import Table, Column, Integer, ForeignKey
from app.infra.db.session import BASE

movie_producers_db = Table(
    "movie_x_producers",
    BASE.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("producer_id", Integer, ForeignKey("producers.id")),
)
