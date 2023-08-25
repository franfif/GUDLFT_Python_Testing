from .conftest import Client


class TestIntegration(Client):
    def test_points_board_after_purchase(self, client, setup_data):
        response = client.get('/points_board')
        # Test points board route
        assert response.status_code == 200
        # Test number points displayed for clubs is as expected
        assert int(setup_data['clubs'][1]['points']) == 4

        # process purchase through route
        response = client.post('/purchase_places', data={'competition': setup_data['competitions'][1]['name'],
                                                         'club': setup_data['clubs'][1]['name'],
                                                         'places': 1})

        # Test points board route
        assert response.status_code == 200

        response = client.get('/points_board')
        # Test points board route
        assert response.status_code == 200
        # Test points left in club
        assert int(setup_data['clubs'][1]['points']) == 3
