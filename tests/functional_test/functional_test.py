import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask
from flask_testing import LiveServerTestCase


# multiprocessing.set_start_method("fork")


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

    def test_login_purchase_update(self):
        driver = webdriver.Chrome()
        driver.get(f'http://127.0.0.1:5000')

        # find email field and enter email to log in
        email_form = driver.find_element(By.NAME, "email")
        email_form.send_keys('john@simplylift.co')
        email_form.send_keys(Keys.RETURN)

        # check login
        assert "Spring Festival 2024" in driver.page_source
        assert "Points available: 13" in driver.page_source

        # find competition book link and follow link
        book_places_link = driver.find_element(By.CSS_SELECTOR, 'li.item-competition a')
        book_places_link.send_keys(Keys.ENTER)

        # check booking page
        assert "Spring Festival 2024" in driver.page_source
        assert "Places available: 25" in driver.page_source

        # find places field in booking form and submit 2
        places_form = driver.find_element(By.NAME, 'places')
        places_form.send_keys('2')
        places_form.send_keys(Keys.RETURN)

        # check result of booking
        assert "Spring Festival 2024" in driver.page_source
        assert "Points available: 11" in driver.page_source

        # find link to points board and follow
        points_board_link = driver.find_element(By.CLASS_NAME, 'points-board-link')
        points_board_link.send_keys(Keys.ENTER)

        # check points booking page
        assert "Points Board" in driver.page_source

        # find club and points in board
        first_club = driver.find_element(By.XPATH, "//td[1]")
        first_club_points = driver.find_element(By.XPATH, "//td[2]")

        # check information in points board
        assert first_club.text == 'Simply Lift'
        assert first_club_points.text == '11'

        driver.quit()
