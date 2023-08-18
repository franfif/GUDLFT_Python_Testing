import pytest
from server import app
import utilities
from utilities.utils import process_purchase, competitions


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize('email, expected_status_code', [('john@simplylift.co', 200), ('wrong.address@test.com', 302)])
def test_login(client, email, expected_status_code):
    response = client.post('/show_summary', data={'email': email})
    assert response.status_code == expected_status_code


# test for BUG02
clubs_for_tests = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
                   {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
                   {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]

competitions_for_tests = [{'name': 'Spring Festival', "date": "2020-10-22 13:30:00", "numberOfPlaces": "25"},
                          {'name': 'Fall Classic', "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
                          {'name': 'Thanksgiving 2023', 'date': '2023-11-23 13:30:00', 'numberOfPlaces': '15'}]

booking_for_tests = {'Spring Festival': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0},
                     'Fall Classic': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0},
                     'Thanksgiving 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0}}


@pytest.mark.parametrize('places_required, expected_status_code', [(300, 302), (1, 200)])
def test_purchase_places(client, places_required, expected_status_code):
    rv = client.post('/purchase_places', data={'competition': "Fall Classic",
                                               'club': 'Iron Temple',
                                               'places': places_required})
    assert rv.status_code == expected_status_code


@pytest.mark.parametrize('club, competition, places_required, processed, messages',
                         [(clubs_for_tests[0], competitions_for_tests[0], 3, True,
                           ["Great-booking complete!"]),
                          (clubs_for_tests[1], competitions_for_tests[1], 400, False,
                           ["You are not allowed to purchase more than 12 places for a single competition.",
                            "There are only 13 places left in this competition.",
                            "You are only able to purchase 4 places for your club."]),
                          ])
def test_process_purchase(club, competition, places_required, processed, messages):
    res_processed, res_messages = process_purchase(club, competition, places_required)
    assert res_processed is processed
    for message in messages:
        assert message in res_messages


def test_process_past_competition(mocker):
    mocker.patch.object(utilities.utils, 'competitions', competitions_for_tests)
    mocker.patch.object(utilities.utils, 'bookings', booking_for_tests)
    res_processed, res_messages = process_purchase(clubs_for_tests[0], competitions_for_tests[1], 4)
    assert res_processed is False


def test_process_current_competition(mocker):
    mocker.patch.object(utilities.utils, 'competitions', competitions_for_tests)
    mocker.patch.object(utilities.utils, 'bookings', booking_for_tests)
    res_processed, res_messages = process_purchase(clubs_for_tests[0], competitions_for_tests[2], 4)
    assert res_processed is True
