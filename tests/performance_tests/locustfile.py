from locust import HttpUser, task


class PerformanceTest(HttpUser):
    @task
    def retrieve_list_of_competitions(self):
        self.client.post('/show_summary', {'email': 'john@simplylift.co'})

    @task
    def update_points_total(self):
        self.client.post('/purchase_places', {'competition': 'Spring Festival 2024',
                                              'club': 'Simply Lift',
                                              'places': 3})
        self.client.post('/show_summary', {'email': 'john@simplylift.co'})
