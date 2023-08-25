import pytest
from server import app
import utilities
import server
from utilities.utils import process_purchase
from .sample_data import mocked_competitions, mocked_clubs, mocked_bookings


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

    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == 302

    def test_logout_after_redirect(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'<h1>Welcome to the GUDLFT Registration Portal!</h1>' in response.data


class TestBook(Client):

    no_club = 'No club'
    no_competition = 'No Competition'

    @pytest.mark.parametrize('club, competition, expected_content, expected_messages',
                             [(mocked_clubs[0]['name'],
                               mocked_competitions[1]['name'],
                               '<title>Booking for',
                               None),
                              (mocked_clubs[0]['name'],
                               mocked_competitions[0]['name'],
                               '<title>Summary | GUDLFT Registration</title>',
                               'Competition is over.'),
                              (no_club,
                               mocked_competitions[1]['name'],
                               '<title>Summary | GUDLFT Registration</title>',
                               'Something went wrong-please try again'),
                              (mocked_clubs[0]['name'],
                               no_competition,
                               '<title>Summary | GUDLFT Registration</title>',
                               'Something went wrong-please try again'),
                              ])
    def test_book_route(self, client, setup_data, club, competition, expected_content, expected_messages):
        response = client.get(f'/book/{competition}/{club}')
        assert response.status_code == 200
        data = response.data.decode()
        assert expected_content in data
        if expected_messages:
            assert expected_messages in data


class TestPurchase(Client):
    @pytest.mark.parametrize('places_required, expected_status_code', [(300, 302), (1, 200), ('', 302)])
    def test_purchase_places(self, client, setup_data, places_required, expected_status_code):
        rv = client.post('/purchase_places', data={'competition': setup_data['competitions'][1]['name'],
                                                   'club': setup_data['clubs'][1]['name'],
                                                   'places': places_required})

        assert rv.status_code == expected_status_code

    @pytest.mark.parametrize('club, competition, places_required, processed, messages',
                             [(mocked_clubs[1], mocked_competitions[1], 400, False,
                               ["You are not allowed to purchase more than 12 places for a single competition.",
                                "There are only 23 places left in this competition.",
                                "You are only able to purchase 4 places for your club."]),
                              (mocked_clubs[1], mocked_competitions[1], 0, False,
                               ["Please enter a number of place to purchase for the competition."]),
                              (mocked_clubs[0], mocked_competitions[1], 3, True,
                               ["Great-booking complete!"]),
                              ])
    def test_process_purchase(self, setup_data, club, competition, places_required, processed, messages):
        res_processed, res_messages = process_purchase(club, competition, places_required)
        assert res_processed is processed
        for message in messages:
            assert message in res_messages

    @pytest.mark.parametrize('club, competition, places_required, expected_processed',
                             [(mocked_clubs[0], mocked_competitions[0], 4, False),
                              (mocked_clubs[0], mocked_competitions[2], 4, True),
                              ])
    def test_process_current_past_competition(self, setup_data, club, competition, places_required, expected_processed):
        res_processed, res_messages = process_purchase(club, competition, places_required)
        assert res_processed is expected_processed

    @pytest.mark.parametrize('club, competition, places_required, expected_processed',
                             [(mocked_clubs[0], mocked_competitions[2],
                               4, True),
                              (mocked_clubs[0], mocked_competitions[2],
                               7, False),
                              (mocked_clubs[0], mocked_competitions[1],
                               13, False),
                              (mocked_clubs[1], mocked_competitions[1],
                               7, False),
                              ])
    def test_update_points(self, setup_data, club, competition, places_required, expected_processed):
        bookings = setup_data['bookings']
        club_expected_points = int(club['points'])
        competition_expected_places = int(competition['numberOfPlaces'])
        booking_expected_places = int(bookings[competition['name']][club['name']])
        if expected_processed:
            club_expected_points -= places_required
            competition_expected_places -= places_required
            booking_expected_places += places_required
        res_processed, res_messages = process_purchase(club, competition, places_required)
        assert res_processed == expected_processed
        assert int(club['points']) == club_expected_points
        assert int(competition['numberOfPlaces']) == competition_expected_places
        assert int(bookings[competition['name']][club['name']]) == booking_expected_places


class TestPointsBoard(Client):
    def test_points_board_route(self, client, setup_data):
        response = client.get('/points_board')
        # Test points board route
        assert response.status_code == 200
        # Test number points displayed for clubs is as expected
        assert b'''<tr>
                    <td>Simply Lift</td>
                    <td>13</td>
                </tr>''' in response.data
