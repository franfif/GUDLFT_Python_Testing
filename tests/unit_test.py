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

# mock load_clubs to return the list I want
# login with an account from mock load_clubs
# mock book()?
# test purchase() with trying to purchase more than the number of points the club has.
# club has 9 points
# club tries to purchase 10 places
# function redirects to book(), with an error message "not enough points"
