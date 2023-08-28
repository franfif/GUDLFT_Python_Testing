from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get('https://www.wikipedia.org/')
assert 'Wikipedia' in driver.title
elem = driver.find_element(By.NAME, "search")
elem.clear()
elem.send_keys("chanson")
elem.send_keys(Keys.RETURN)
assert "French songs of late" in driver.page_source
driver.close()
