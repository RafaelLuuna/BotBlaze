from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os

class driver_class:

    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(script_dir,'chrome/chromedriver/chromedriver.exe')
        chrome_path = os.path.join(script_dir,'chrome/win64-114.0.5735.90/chrome-win64/chrome.exe')

        ChromeOptions = Options()
        ChromeOptions.binary_location = chrome_path
        chrome_service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=chrome_service, options=ChromeOptions)


    def initialize_browser(self):
        print('[Inicialndo chromedriver]')
        self.driver.get('https://blaze-1.com/pt/games/double')
    
    def incluir_aposta(self, valor):
        return 0
    
    def apostar(self, cor):
        return 0
    
    def get_saldo(self):
        return 0
