from unittest.mock import patch
from config import config

@patch("app.controllers.intervals_controller.IntervalsController.get_award_intervals", return_value={
    "min": [
        {
            "producer": "Joel Silver",
            "interval": 1,
            "previousWin": 1990,
            "followingWin": 1991
        }
    ],
    "max": [
        {
            "producer": "Matthew Vaughn",
            "interval": 13,
            "previousWin": 2002,
            "followingWin": 2015
        }
    ]
})
@patch("app.controllers.load_file_controller.LoadFileController.run", return_value=None)
@patch("app.infra.file_module.file_utils.FileUtils.read_csv", return_value=[
    {"year": 1990, "title": "Movie A", "studios": "Studio", "producers": ["Joel Silver"], "winner": "yes"},
    {"year": 1991, "title": "Movie B", "studios": "Studio", "producers": ["Joel Silver"], "winner": "yes"},
    {"year": 2002, "title": "Movie C", "studios": "Studio", "producers": ["Matthew Vaughn"], "winner": "yes"},
    {"year": 2015, "title": "Movie D", "studios": "Studio", "producers": ["Matthew Vaughn"], "winner": "yes"},
])
def test_intervals_success(mock_read_csv, mock_load_file, mock_find_intervals, setup_database, setup_db_for_test, client):
    """Testa o /intervals com ganhadores - sucesso."""

    headers = {"x-api-key": config.api_key}
    response = client.get("/v1/intervals", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert "min" in body
    assert "max" in body
    assert len(body["min"]) > 0
    assert len(body["max"]) > 0


@patch("app.controllers.intervals_controller.IntervalsController.get_award_intervals", side_effect=Exception("Unexpected error"))
@patch("app.controllers.load_file_controller.LoadFileController.run", return_value=None)
@patch("app.infra.file_module.file_utils.FileUtils.read_csv", return_value=[
    {"year": 1990, "title": "Movie A", "studios": "Studio", "producers": ["Joel Silver"], "winner": "yes"},
])
def test_intervals_unexpected_error(mock_read_csv, mock_load_file, mock_find_intervals, setup_database, setup_db_for_test, client):
    """Testa o /intervals quando ocorre um erro inesperado."""

    headers = {"x-api-key": config.api_key}
    response = client.get("/v1/intervals", headers=headers)

    assert response.status_code >= 500  # Pode ser 500, 502, 503 dependendo da sua app
    body = response.json()
    assert "detail" in body

@patch("app.controllers.intervals_controller.IntervalsController.get_award_intervals", return_value={
    "min": [],
    "max": []
})
@patch("app.controllers.load_file_controller.LoadFileController.run", return_value=None)
@patch("app.infra.file_module.file_utils.FileUtils.read_csv", return_value=[
    {"year": 1990, "title": "Movie A", "studios": "Studio", "producers": ["Joel Silver"], "winner": "no"},
    {"year": 1991, "title": "Movie B", "studios": "Studio", "producers": ["Joel Silver"], "winner": "no"},
])
def test_intervals_no_winners(mock_read_csv, mock_load_file, mock_find_intervals, setup_database, setup_db_for_test, client):
    """Testa o /intervals sem ganhadores."""

    headers = {"x-api-key": config.api_key}
    response = client.get("/v1/intervals", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["min"] == []
    assert body["max"] == []
