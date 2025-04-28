from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///:memory:"
BASE = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

db_session = Session()

def create_all_tables():
    from app.infra.db.award_entity import AwardDB
    from app.infra.db.movie_entity import MovieDB
    from app.infra.db.movie_x_producers_entity import movie_producers_db
    from app.infra.db.studio_entity import StudioDB
    from app.infra.db.producer_entity import ProducerDB

    try:
        BASE.metadata.create_all(engine)

    except Exception as e:

        raise Exception(f"ERRO AO VERIFICAR BANCO DE DADOS: {e}")
