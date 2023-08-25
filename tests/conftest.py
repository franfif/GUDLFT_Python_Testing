import pytest
from server import app

from utilities import utils
from .sample_data import competitions_for_tests, clubs_for_tests, bookings_for_tests
import server


class Client:
    @staticmethod
    @pytest.fixture
    def client():
        with app.test_client() as client:
            yield client


@pytest.fixture(scope='function')
def setup_data(mocker):
    mocked_competitions = competitions_for_tests()
    mocked_clubs = clubs_for_tests()
    mocked_bookings = bookings_for_tests()
    mocker.patch.object(server, 'competitions', mocked_competitions)
    mocker.patch.object(server, 'clubs', mocked_clubs)
    mocker.patch.object(utils, 'competitions', mocked_competitions)
    mocker.patch.object(utils, 'clubs', mocked_clubs)
    mocker.patch.object(utils, 'bookings', mocked_bookings)
    yield {'competitions': mocked_competitions,
           'clubs': mocked_clubs,
           'bookings': mocked_bookings}
