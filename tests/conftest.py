import pytest
import os
from pathlib import Path
from main import app
from fastapi.testclient import TestClient
from app.infra.db.movie_entity import MovieDB
from app.infra.db.producer_entity import ProducerDB
from app.infra.db.studio_entity import StudioDB
from app.infra.db.award_entity import AwardDB
from app.infra.db.movie_x_producers_entity import movie_producers_db
from app.infra.db.session import BASE, engine_test, db_session_test
from app.infra.db import session as session_module


session_module.engine = engine_test
session_module.db_session = db_session_test

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria o banco test.db antes da sessão de testes e deleta no fim."""
    if os.path.exists("test.db"):
        os.remove("test.db")
    BASE.metadata.create_all(bind=engine_test)
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture(autouse=True)
def reset_db():
    """Reseta todas as tabelas antes de cada teste."""
    BASE.metadata.drop_all(bind=engine_test)
    BASE.metadata.create_all(bind=engine_test)
    yield

@pytest.fixture
def client(reset_db):
    """Retorna um TestClient."""
    return TestClient(app)

@pytest.fixture
def setup_folders():
    """Cria a pasta de testes."""
    base_path = Path("app") / "infra" / "bucket" / "test_data"
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path

@pytest.fixture
def create_csv():
    """Helper para criar arquivos CSV rapidamente."""
    def _create_csv(directory, filename, content):
        fullpath = directory / filename
        with open(fullpath, "w", encoding="utf-8") as f:
            f.write(content)
        return fullpath
    return _create_csv

@pytest.fixture
def setup_db_for_test():
    """Insere dados iniciais no banco para integração."""
    studio = StudioDB(name="Studio")
    producer = ProducerDB(name="Producer 1")

    db_session_test.add(studio)
    db_session_test.add(producer)
    db_session_test.flush()

    movie1 = MovieDB(title="Movie 1", studio_id=studio.id)
    movie2 = MovieDB(title="Movie 2", studio_id=studio.id)

    db_session_test.add_all([movie1, movie2])
    db_session_test.flush()

    award1 = AwardDB(movie_id=movie1.id, year=1980, winner="yes")
    award2 = AwardDB(movie_id=movie2.id, year=1982, winner="yes")

    db_session_test.add_all([award1, award2])

    db_session_test.execute(movie_producers_db.insert(), [
        {"movie_id": movie1.id, "producer_id": producer.id},
        {"movie_id": movie2.id, "producer_id": producer.id},
    ])

    db_session_test.commit()
