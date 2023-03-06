import requests
import json


def test_get_health():
    response = requests.get("http://localhost:5000/_health")
    data = json.loads(response.text)
    assert response.status_code == 200
    assert data["success"] == "True"
