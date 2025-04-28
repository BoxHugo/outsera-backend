import pytest
import os
import shutil
from fastapi.testclient import TestClient
from ..main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def setup_folders(tmp_path):
    """Cria estrutura de pastas isolada para testes."""
    path = tmp_path / "test_data"
    input_path = path / "input"
    processed_path = path / "processed"
    input_path.mkdir(parents=True)
    processed_path.mkdir(parents=True)
    return path

def create_csv(directory, filename, content):
    """Helper para criar CSVs."""
    fullpath = directory / filename
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content)
    return fullpath
