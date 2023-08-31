import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask
from flask_testing import LiveServerTestCase


multiprocessing.set_start_method("fork")


class TestPurchase(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        driver = webdriver.Chrome()
        driver.get(f'http://127.0.0.1:5000')
        assert "GUDLFT" in driver.title

        driver.quit()
