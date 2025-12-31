from django.test import Client


def test_health_returns_200():
    client = Client()
    response = client.get("/health/")
    assert response.status_code == 200
