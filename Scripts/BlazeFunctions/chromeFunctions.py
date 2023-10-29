from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)


class driver_class:

    def initialize_browser(self, url='https://blaze-4.com/pt/games/double'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(script_dir,'chrome/chromedriver/chromedriver.exe')
        chrome_path = os.path.join(script_dir,'chrome/win64-114.0.5735.90/chrome-win64/chrome.exe')

        ChromeOptions = Options()
        ChromeOptions.binary_location = chrome_path
        chrome_service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=chrome_service, options=ChromeOptions)
        print('[Inicialndo chromedriver]')
        self.driver.get(url)

    def apostar(self, Cor, Valor):
        print('[Apostando no driver]')
        try:
            input_element = self.driver.find_element(By.CLASS_NAME, 'input-field')
            if(Valor > 0):
                input_element.send_keys(Valor)
            else:
                input_element.send_keys(1)
        except Exception as e:
            print(f"Erro ao incluir aposta: {e}")
        match Cor:
            case 0:
                CorPath = 2
            case 1:
                CorPath = 1
            case 2:
                CorPath = 3
        Path = f'//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[{CorPath}]'
        try:
            ColorButton = self.driver.find_element(By.XPATH, Path)
            ColorButton.click()
        except Exception as e:
            print(f"Erro ao apostar: {e}")
        wait = WebDriverWait(self.driver, 60)
        PlayButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button')))
        try:
            PlayButton.click()
        except Exception as e:
            print(f"Erro ao apostar: {e}")

    
    def get_saldo(self):
        try:
            div_element = self.driver.find_element(By.CLASS_NAME, 'currency')
            return div_element.text[3:].replace(".","").replace(",",".")
        except NoSuchElementException as e:
            return 'Saldo não localizado'
        except Exception as e:
            print(f"Erro ao ler saldo da plataforma: {e}")
            return 0
