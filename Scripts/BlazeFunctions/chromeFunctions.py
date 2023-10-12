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
        self.driver.get('https://blaze-4.com/pt/games/double')
    
    def incluir_aposta(self, Valor):
        try:
            input_element = self.driver.find_element(By.CLASS_NAME, 'input-field')
            if(Valor > 0):
                input_element.send_keys(Valor)
            else:
                input_element.send_keys(1)
        except Exception as e:
            print(f"Erro ao incluir aposta: {e}")

    def selecionar_cor(self, Cor):
        match Cor:
            case 0:
                CorPath = 2
            case 1:
                CorPath = 1
            case 2:
                CorPath = 3
        Path = f'//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[{CorPath}]'
        try:
            click_button = self.driver.find_element(By.XPATH, Path)
            click_button.click()
        except Exception as e:
            print(f"Erro ao apostar: {e}")
    
    def apostar(self, cor):
        try:
            wait = WebDriverWait(self.driver, 10)
            click_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button')))
            click_button.click()
        except Exception as e:
            print(f"Erro ao apostar: {e}")

    
    def get_saldo(self):
        try:
            div_element = self.driver.find_element(By.CLASS_NAME, 'currency')
            return div_element.text[3:].replace(".","").replace(",",".")
        except Exception as e:
            print(f"Erro ao ler saldo da plataforma: {e}")
            return 0


