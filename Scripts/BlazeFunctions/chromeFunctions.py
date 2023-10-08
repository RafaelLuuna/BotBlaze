from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class driver_class:

    driver = ''

    def __init__(self):
        ChromeOptions = Options()
        chrome_service = Service()
        self.driver = webdriver.Chrome(service=chrome_service, options=ChromeOptions)


    def initialize_browser(self):
        print('[Inicialndo chromedriver]')
        self.driver.get('https://blaze-1.com/pt/games/double')
