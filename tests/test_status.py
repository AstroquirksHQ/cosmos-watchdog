def test_health_endpoint(client):
    response = client.get("/_health")
    assert response.status_code == 200
    assert response.get_json() == {"success": "True"}
