import pytest
from server import app

from utilities import utils
from .sample_data import mocked_competitions, mocked_clubs, mocked_bookings
import server


class Client:
    @staticmethod
    @pytest.fixture
    def client():
        with app.test_client() as client:
            yield client


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
