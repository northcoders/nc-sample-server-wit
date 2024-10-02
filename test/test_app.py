import pytest
from fastapi.testclient import TestClient
from src.api.app import app, get_doughnut_data
from unittest.mock import patch
from data import doughnuts_expected, doughnuts_results


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.mark.describe("Routes")
@pytest.mark.it("/api/doughnuts")
def test_get_doughnuts_returns_doughnuts(client):
    with patch("src.api.app.get_doughnut_data", return_value=doughnuts_results):
        result = client.get("/api/doughnuts")
        assert result.json() == doughnuts_expected


@pytest.mark.describe("Routes")
@pytest.mark.it("/api/doughnuts/{doughnut_id}")
def test_doughnuts_id(client):
    with patch("src.api.app.get_doughnut_data", return_value=doughnuts_results):
        result = client.get("/api/doughnuts/1")
        assert result.json() == doughnuts_expected[0]


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Healthcheck response")
def test_healthcheck(client):
    result = client.get("/api/healthcheck")
    assert result.status_code == 200
    assert result.json() == "Application is healthy"


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Error response for missing doughnut")
def test_doughnut_error_integration(client):
    result = client.get("/api/doughnuts/88")
    assert result.status_code == 404
    assert result.json() == {"detail": "No such doughnut: 88"}


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Error response for no doughnuts")
def test_doughnut_error_integration_all(client):
    with patch("src.api.app.get_doughnut_data", return_value=[]):
        result = client.get("/api/doughnuts")
        assert result.status_code == 404
        assert result.json() == {"detail": "No doughnuts"}


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Error response for doughnuts server error")
def test_doughnut_server_error_integration_all(client):
    with patch("src.api.app.get_doughnut_data", side_effect=RuntimeError):
        result = client.get("/api/doughnuts")
        assert result.status_code == 500


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Error response for single doughnut server error")
def test_doughnut_server_error_integration_single(client):
    with patch("src.api.app.get_doughnut_data", side_effect=RuntimeError):
        result = client.get("/api/doughnuts/3")
        assert result.status_code == 500
