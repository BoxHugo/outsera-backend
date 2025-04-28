import pytest
from tests.conftest import create_csv

def test_intervals_success(client, setup_folders):
    """ Testa endpoint /intervals caso de sucesso """

    content = "year;title;studios;producers;winner\n1980;Movie 1;Studio;Producer 1;yes\n1982;Movie 2;Studio;Producer 1;yes"
    create_csv(setup_folders / "input", "file.csv", content)

    response = client.get("/intervals")
    
    assert response.status_code == 200
    body = response.json()
    assert "min" in body
    assert "max" in body
    assert len(body["min"]) > 0
    assert len(body["max"]) > 0

def test_intervals_no_winners(client, setup_folders):
    """ Testa endpoint /intervals caso sem ganhadores """

    content = "year;title;studios;producers;winner\n1980;Movie 1;Studio;Producer 1;no"
    create_csv(setup_folders / "input", "file.csv", content)

    response = client.get("/intervals")
    body = response.json()
    
    assert response.status_code == 200
    assert body["min"] == []
    assert body["max"] == []

def test_intervals_missing_file(client, setup_folders):
    """ Testa endpoint /intervals caso sem arquivo consumido """

    response = client.get("/intervals")
    
    assert response.status_code == 422 or response.status_code == 500

def test_unexpected_error(client, setup_folders, monkeypatch):
    """ Erro inesperado."""

    def broken_read_csv(*args, **kwargs):
        raise Exception("Simulated Error")

    from app.infra.file_module.file_utils import FileUtils

    monkeypatch.setattr(FileUtils, "read_csv", broken_read_csv)

    response = client.get("/intervals")
    
    assert response.status_code >= 500
