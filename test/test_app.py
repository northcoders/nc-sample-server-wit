import pytest
from fastapi.testclient import TestClient
from src.api.app import app
from unittest.mock import patch
from src.data.sql import query_strings
from data import (
    categories_result,
    multiple_sales,
    products_expected,
    single_sale,
    products_results,
    users_results,
    user_sales_results,
)
from src.api.helpers import DBConnectionException


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


def dummy_process(query, **kwargs):
    if query == query_strings["categories"]:
        return categories_result
    elif query == query_strings["products"]:
        return products_results
    elif query == query_strings["product"]:
        ((key, param),) = kwargs.items()
        result = [p for p in products_results if p["product_id"] == int(param)]
        assert len(result) == 1
        return result
    elif query == query_strings["users"]:
        return users_results


@pytest.mark.describe("Routes")
@pytest.mark.it("/api/categories")
def test_categories(client):
    with patch("src.api.app.process_query", side_effect=dummy_process):
        result = client.get("/api/categories")
        assert result.json() == categories_result


@pytest.mark.describe("Routes")
@pytest.mark.it("/api/categories 500 response")
@patch("src.api.helpers.get_db_connection")
def test_categories_500(mock_conn, client):
    mock_conn.side_effect = DBConnectionException("Awful error")
    result = client.get("/api/categories")
    assert result.status_code == 500
    assert result.json() == {
        "detail": "There was an error connecting to the database: Awful error"
    }


@pytest.mark.describe("Routes")
@pytest.mark.it("/api/products")
def test_get_products_returns_products(client):
    with patch("src.api.app.process_query", side_effect=dummy_process):
        result = client.get("/api/products")
        assert result.json() == products_expected


@pytest.mark.describe("Routes")
@pytest.mark.it("/api/products/{product_id}")
def test_products_id(client):
    with patch("src.api.app.process_query", side_effect=dummy_process):
        result = client.get("/api/products/7")
        assert result.json() == products_expected[1]


@pytest.mark.describe("Routes")
@pytest.mark.it("/users")
def test_users(client):
    with patch("src.api.app.process_query", side_effect=dummy_process):
        result = client.get("/api/users")
        res_list = result.json()
        assert len(res_list) == 3
        assert res_list[0]["first_name"] == "Afton"
        assert res_list[1]["last_name"] == "Bergnaum"
        assert "email" not in res_list[1]


@pytest.mark.describe("Routes")
@pytest.mark.it("/users/{user_id}/average_spend - single purchase")
def test_get_user_average_calculates_average_one_purchase(client):
    patch_return = single_sale
    with patch("src.api.app.process_query", return_value=patch_return) as mock_process:
        expected = {"user_id": 10, "average_spend": 202.00}
        expected_query = query_strings["sales_average"]
        result = client.get("/api/users/10/average_spend")
        mock_process.assert_called_once_with(expected_query, user_id=10)
        assert result.json() == expected


@pytest.mark.describe("Routes")
@pytest.mark.it("/users/{user_id}/average_spend - many purchases")
def test_get_user_average_correctly_calculates_average(client):
    patch_return = multiple_sales
    with patch("src.api.app.process_query", return_value=patch_return):
        expected = {"user_id": 10, "average_spend": 118.0}
        result = client.get("/api/users/10/average_spend")
        assert result.json() == expected


@pytest.mark.describe("Routes")
@pytest.mark.it("/users/{user_id}/sales?...")
@patch("src.api.app.check_user", return_value=[3])
def test_user_sales(mock_check, client):
    with patch("src.api.app.process_query", return_value=user_sales_results):
        result = client.get(
            "/api/users/3/sales?date_from=2022-10-01&date_to=2022-11-01"
        )
        result_list = result.json()
        expected = {
            "user_id": 7,
            "sales_id": 373,
            "product_id": 9,
            "transaction_ts": "2022-10-06T11:34:50.096Z",
            "product_title": "Bespoke Wooden Bike",
            "product_cost": 393.000000000000000000000000000000,
            "category": "Garden",
            "num_items": 1,
        }
        assert len(result_list) == 2
        assert result_list[1] == expected
        assert result_list[0]["sales_id"] == 408


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Correct response for user sales")
def test_user_sales_integration(client):
    result = client.get("/api/users/3/sales?date_from=2022-10-01&date_to=2022-10-11")
    result_list = result.json()
    assert len(result_list) == 5
    sale_ids = {s["sales_id"] for s in result_list}
    assert sale_ids == set([307, 519, 407, 421, 46])


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Empty response for sales dates out of range")
def test_sales_dates(client):
    result = client.get("/api/users/3/sales?date_from=2023-10-01&date_to=2023-10-11")
    result_list = result.json()
    assert len(result_list) == 0


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Error response for nonexistent user")
def test_nonexistent_user(client):
    res = client.get("/api/users/777/sales?date_from=2022-10-01&date_to=2022-10-11")
    assert res.status_code == 404
    assert res.json() == {
        "detail": "No instance of user was found in the database with id 777."
    }


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Latest sales for user")
def test_latest(client):
    result = client.get("/api/users/7/sales/latest")
    result_list = result.json()
    assert len(result_list) == 5
    assert result_list[0]["transaction_ts"] == "2023-01-23T10:08:26.341000"
    assert result_list[4]["product_title"] == "Refined Steel Sausages"
    err = client.get("/api/users/777/sales/latest")
    assert err.status_code == 404
    assert err.json() == {
        "detail": "No instance of user was found in the database with id 777."
    }


@pytest.mark.describe("Integration tests")
@pytest.mark.it("Error response for missing product")
def test_product_error_integration(client):
    result = client.get("/api/products/88")
    assert result.status_code == 404
    assert result.json() == {
        "detail": "No instance of product was found in the database with id 88."
    }
