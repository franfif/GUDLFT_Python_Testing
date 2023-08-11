import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize('email', ['john@simplylift.co', 'admin@irontemple.com'])
def test_login_registered_user(client, email):
    response = client.post('/show_summary', data={'email': email})
    expected_value = 200
    assert response.status_code == expected_value


@pytest.mark.parametrize('email', ['wrong.address@test.com', 'not.an.address'])
def test_login_unregistered_user(client, email):
    response = client.post('/show_summary', data={'email': email})
    expected_value = 302
    assert response.status_code == expected_value
