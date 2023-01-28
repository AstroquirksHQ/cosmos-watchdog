from run import app
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
