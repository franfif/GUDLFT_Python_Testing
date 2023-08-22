import pytest
from server import app
import utilities
import server
from utilities.utils import process_purchase


class Client:
    @staticmethod
    @pytest.fixture
    def client():
        with app.test_client() as client:
            yield client


class TestLogin(Client):
    @pytest.mark.parametrize('email, expected_status_code', [('john@simplylift.co', 200),
                                                             ('wrong.address@test.com', 302)])
    def test_login(self, client, email, expected_status_code):
        response = client.post('/show_summary', data={'email': email})
        assert response.status_code == expected_status_code


class DataForTests:
    @pytest.fixture
    def setup_data(self, mocker):
        mocked_clubs = self.clubs_for_tests()
        mocked_competitions = self.competitions_for_tests()
        mocked_bookings = self.bookings_for_tests()
        mocker.patch.object(server, 'competitions', mocked_competitions)
        mocker.patch.object(server, 'clubs', mocked_clubs)
        mocker.patch.object(utilities.utils, 'competitions', mocked_competitions)
        mocker.patch.object(utilities.utils, 'bookings', mocked_bookings)
        mocker.patch.object(utilities.utils, 'clubs', mocked_clubs)

    @staticmethod
    def clubs_for_tests():
        return [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
                {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
                {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]

    @staticmethod
    def competitions_for_tests():
        return [{'name': 'Spring Festival 2023', "date": "2023-04-22 13:30:00", "numberOfPlaces": "25"},
                {'name': 'Fall Classic 2023', "date": "2023-10-22 13:30:00", "numberOfPlaces": "13"},
                {'name': 'Thanksgiving 2023', 'date': '2023-11-23 13:30:00', 'numberOfPlaces': '15'}]

    @staticmethod
    def bookings_for_tests():
        return {'Spring Festival 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0},
                'Fall Classic 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0},
                'Thanksgiving 2023': {'Simply Lift': 0, 'Iron Temple': 0, 'She Lifts': 0}}


class TestPurchase(DataForTests, Client):
    @pytest.mark.parametrize('places_required, expected_status_code', [(300, 302), (1, 200)])
    def test_purchase_places(self, client, setup_data, places_required, expected_status_code):
        rv = client.post('/purchase_places', data={'competition': self.competitions_for_tests()[1]['name'],
                                                   'club': self.clubs_for_tests()[1]['name'],
                                                   'places': places_required})

        assert rv.status_code == expected_status_code

    @pytest.mark.parametrize('club, competition, places_required, processed, messages',
                             [(DataForTests.clubs_for_tests()[1], DataForTests.competitions_for_tests()[1], 400, False,
                               ["You are not allowed to purchase more than 12 places for a single competition.",
                                "There are only 13 places left in this competition.",
                                "You are only able to purchase 4 places for your club."]),
                              (DataForTests.clubs_for_tests()[0], DataForTests.competitions_for_tests()[1], 3, True,
                               ["Great-booking complete!"]),
                              ])
    def test_process_purchase(self, setup_data, club, competition, places_required, processed, messages):
        res_processed, res_messages = process_purchase(club, competition, places_required)
        assert res_processed is processed
        for message in messages:
            assert message in res_messages

    @pytest.mark.parametrize('club, competition, places_required, expected_processed',
                             [(DataForTests.clubs_for_tests()[0], DataForTests.competitions_for_tests()[0], 4, False),
                              (DataForTests.clubs_for_tests()[0], DataForTests.competitions_for_tests()[2], 4, True),
                              ])
    def test_process_current_past_competition(self, setup_data, club, competition, places_required, expected_processed):
        res_processed, res_messages = process_purchase(club, competition, places_required)
        assert res_processed is expected_processed
