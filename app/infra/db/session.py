from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///:memory:"
DATABASE_URL_TEST = "sqlite:///./test.db"

BASE = declarative_base()

engine = create_engine(DATABASE_URL, echo=False)
engine_test = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})

Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

db_session = Session()
db_session_test = TestingSession()

def create_all_tables():
    """Cria as tabelas no banco de produção (memory)."""
    from app.infra.db.award_entity import AwardDB
    from app.infra.db.movie_entity import MovieDB
    from app.infra.db.movie_x_producers_entity import movie_producers_db
    from app.infra.db.studio_entity import StudioDB
    from app.infra.db.producer_entity import ProducerDB

    try:
        BASE.metadata.create_all(engine)
    except Exception as e:
        raise Exception(f"ERRO AO CRIAR TABELAS NO PROD: {e}")

def create_all_tables_test():
    """Cria as tabelas no banco de testes (test.db)."""
    from app.infra.db.award_entity import AwardDB
    from app.infra.db.movie_entity import MovieDB
    from app.infra.db.movie_x_producers_entity import movie_producers_db
    from app.infra.db.studio_entity import StudioDB
    from app.infra.db.producer_entity import ProducerDB

    try:
        BASE.metadata.create_all(engine_test)
    except Exception as e:
        raise Exception(f"ERRO AO CRIAR TABELAS NO TESTE: {e}")
