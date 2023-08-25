import pytest

from utilities import utils
from .sample_data import mocked_competitions, mocked_clubs, mocked_bookings
import server


@pytest.fixture(scope='function')
def setup_data(mocker):
    mocker.patch.object(server, 'competitions', mocked_competitions)
    mocker.patch.object(server, 'clubs', mocked_clubs)
    mocker.patch.object(utils, 'competitions', mocked_competitions)
    mocker.patch.object(utils, 'clubs', mocked_clubs)
    mocker.patch.object(utils, 'bookings', mocked_bookings)
    yield {'competitions': mocked_competitions,
           'clubs': mocked_clubs,
           'bookings': mocked_bookings}


# def clubs_for_tests():
#     return [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
#             {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
#             {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]
#
#
# def competitions_for_tests():
#     return [{'name': 'Spring Festival 2023', "date": "2023-04-22 13:30:00", "numberOfPlaces": "25"},
#             {'name': 'Fall Classic 2023', "date": "2023-10-22 13:30:00", "numberOfPlaces": "23"},
#             {'name': 'Thanksgiving 2023', 'date': '2023-11-23 13:30:00', 'numberOfPlaces': '5'}]
#
#
# def bookings_for_tests():
#     return {'Spring Festival 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0},
#             'Fall Classic 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0},
#             'Thanksgiving 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0}}
#
#
# mocked_competitions = competitions_for_tests()
# mocked_clubs = clubs_for_tests()
# mocked_bookings = bookings_for_tests()
