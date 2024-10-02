"""Defines the entrypoint and functionality for the API routes.

The API server is started by running this file directly
from Python. 

Run:
    make start-server
from the root directory.

Then navigate to localhost:8000/docs to see the OpenAPI documentation,
or navigate to localhost:8000/api/<route> to see an API request result.
"""
from fastapi import FastAPI, HTTPException
import json
from src.api.helpers import logger, ItemNotFoundException


PORT = 8000

app = FastAPI()


@app.get("/api/healthcheck")
def get_healthcheck() -> str:
    """Simple healthcheck endpoint."""
    return "Application is healthy"


@app.get("/api/doughnuts")
def get_doughnuts() -> list[dict]:
    """Gets list of all doughnuts.

    If no doughnuts, returns empty list.

    Returns:
        Result of query.

        Example:
        [
            {
                "doughnut_id" : 1,
                "doughnut_type" : "Choccy Delight",
                "price" : 1.38,
                "calories" : 800,
                "contains_nuts" : true
                }
        ]
    """
    try:
        results = get_doughnut_data()
        if len(results) == 0:
            raise ItemNotFoundException("doughnuts")
        modified = [
            {"doughnut_id" if k == "id" else k: v for k, v in result.items()}
            for result in results
        ]
        return modified
    except ItemNotFoundException as i:
        message = "No doughnuts"
        logger.info(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as e:
        logger.info(f"Unexpected exception in /doughnuts endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/doughnuts/{doughnut_id}")
def get_doughnut(doughnut_id: int) -> dict:
    """Gets details of specific doughnut.

    Returns details of specific doughnut. If no such doughnut,
    returns error response.

    Args:
        doughnut_id: the identifier for the doughnut.
    Returns:
        Result of query.

        Example:
        {
            "id" : 1,
            "doughnut_type" : "Choccy Delight",
            "price" : 1.38,
            "calories" : 800,
            "contains_nuts" : true
            }
    """
    try:
        results = get_doughnut_data()
        modified = [
            {"doughnut_id" if k == "id" else k: v for k, v in result.items()}
            for result in results
        ]
        return [r for r in modified if r["doughnut_id"] == doughnut_id][0]
    except (KeyError, IndexError) as k:
        message = f"No such doughnut: {doughnut_id}"
        logger.info(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as e:
        logger.info(f"Unexpected exception in /doughnuts/id endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_doughnut_data():
    with open("src/data/doughnuts.json", "r") as f:
        data = json.load(f)
    return data["doughnuts"]
