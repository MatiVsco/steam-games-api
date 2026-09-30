from fastapi.testclient import TestClient
from steam_games import app
from services import fetch_games
from unittest.mock import patch
import requests
import pytest


client = TestClient(app)


@pytest.fixture
def fake_games():
    return [
        {
            "id": 730,
            "name": "Counter-Strike 2",
            "price": 0,
            "release_date": "Aug 21, 2012"
        },
        {
            "id": 570,
            "name": "Dota 2",
            "price": 0,
            "release_date": "Jul 9, 2013"
        }
    ]


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_games(fake_games):
    with patch("steam_games.fetch_games", return_value=fake_games):
        response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == fake_games


def test_get_game_by_appid(fake_games):
    with patch("steam_games.fetch_games", return_value=fake_games):
        response = client.get("/games/730")

    assert response.status_code == 200

    game_data = response.json()

    assert game_data["id"] == 730
    assert game_data["name"] == "Counter-Strike 2"
    assert game_data["price"] == 0
    assert game_data["release_date"] == "Aug 21, 2012"


def test_game_not_found(fake_games):
    with patch("steam_games.fetch_games", return_value=fake_games):
        response = client.get("/games/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}


def test_limit():
    fake_games = [
        {"id": 1, "name": "Game 1", "price": 10, "release_date": "2020"},
        {"id": 2, "name": "Game 2", "price": 20, "release_date": "2021"},
        {"id": 3, "name": "Game 3", "price": 30, "release_date": "2022"},
        {"id": 4, "name": "Game 4", "price": 40, "release_date": "2023"},
        {"id": 5, "name": "Game 5", "price": 50, "release_date": "2024"},
    ]

    with patch("steam_games.fetch_games", return_value=fake_games):
        response = client.get("/games?limit=3")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_invalid_limit():
    response = client.get("/games?limit=-1")

    assert response.status_code == 422
    assert "detail" in response.json()


def test_invalid_sort_by():
    response = client.get("/games?sort_by=banana")

    assert response.status_code == 422
    assert "detail" in response.json()


def test_fetch_games():
    fake_response = {
        "730": {
            "success": True,
            "data": {
                "name": "Counter-Strike 2",
                "price_overview": {
                    "final": 1999
                },
                "release_date": {
                    "date": "Aug 21, 2012"
                }
            }
        }
    }

    with patch("services.appids", [730]):
        with patch("services.requests.get") as mock_get:
            mock_get.return_value.json.return_value = fake_response
            mock_get.return_value.raise_for_status.return_value = None

            games = fetch_games()

    assert games == [
        {
            "id": 730,
            "name": "Counter-Strike 2",
            "price": 19.99,
            "release_date": "Aug 21, 2012"
        }
    ]


def test_fetch_games_skips_unsuccessful_game():
    fake_response = {
        "730": {
            "success": False
        }
    }

    with patch("services.appids", [730]):
        with patch("services.requests.get") as mock_get:
            mock_get.return_value.json.return_value = fake_response
            mock_get.return_value.raise_for_status.return_value = None

            games = fetch_games()

    assert games == []


def test_fetch_games_skips_request_error():
    with patch(
        "services.appids",
        [730]
    ):
        with patch(
            "services.requests.get",
            side_effect=requests.RequestException
        ):
            games = fetch_games()

    assert games == []


def test_fetch_games_skips_invalid_json():
    with patch("services.appids", [730]):
        with patch("services.requests.get") as mock_get:
            mock_get.return_value.raise_for_status.return_value = None
            mock_get.return_value.json.side_effect = ValueError

            games = fetch_games()

    assert games == []