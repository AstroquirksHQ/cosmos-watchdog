import requests
import json


def test_get_health():
    response = requests.get("http://localhost:5000/_health")
    assert response.status_code == 200
    data = json.loads(response.text)
    assert data["success"] == "True"
