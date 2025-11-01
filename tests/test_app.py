import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # now Python can find your app.py


def test_forecast_route():
    # create a test client for the Flask app
    client = app.test_client()

    # send GET request to /forecast endpoint
    response = client.get("/forecast")

    # check that the response is successful
    assert response.status_code == 200

    # check that response has valid JSON
    data = response.get_json()
    assert "predictions" in data
    assert isinstance(data["predictions"], list)
    assert len(data["predictions"]) > 0

    # ensure each prediction has required keys
    for item in data["predictions"]:
        assert "date" in item
        assert "day" in item
        assert "predicted_AQI" in item
