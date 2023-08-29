import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask
from flask_testing import LiveServerTestCase
import unittest
import server


multiprocessing.set_start_method("fork")

# class found on the Internet, not sure of the use
# class MyLiveServerTestCase(LiveServerTestCase):
#     def __call__(self, *args, **kwargs):
#         self._spawn_live_server()
#         self._port_value = self.port
#         super(MyLiveServerTestCase, self).__call__(*args, **kwargs)


# class TestPurchase(MyLiveServerTestCase):
class TestPurchase(LiveServerTestCase):

    # To go with the class MyLiveServerTestCase
    # def _spawn_live_server(self):
    #     self.port = self.get_http_port()
    #     self.base_url = f'http://localhost:{self.port}'
    #     self.app = server.app
    #     self.app.config['TESTING'] = True
    #     self.server = self.app.run(port=self.port, use_reloader=False, threaded=True)

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    # to go with the method _spawn_live_server()
    # def get_http_port(self):
    #     return 5001

    def test_server_is_up_and_running(self):
        driver = webdriver.Chrome()
        driver.get(self.get_server_url())
        # give me time to see by myself if the server is running,
        # before I try any test
        time.sleep(15)
        driver.quit()
