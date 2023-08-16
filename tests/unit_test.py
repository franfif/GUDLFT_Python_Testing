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


# test for BUG02
clubs_for_tests = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
                   {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
                   {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]


def test_purchase_too_many_places(client):
    rv = client.post('/purchase_places', data={'competition': "Spring Festival",
                                               'club': 'Simply Lift',
                                               'places': 15})
    data = rv.data.decode()
    assert rv.status_code == 302
    assert data.find("Your club does not have enough places.") != -1

