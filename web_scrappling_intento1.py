from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

def main ():
    # Configurar Selenium con el Webdriver
    service=Service(ChromeDriverManager().install())
    option=webdriver.ChromeOptions()
    # option.add_argument("--headless")
    driver= Chrome(service=service, options=option)

    driver.get("https://www.elcorteingles.es/cine/accion-y-aventuras/") # Estamos configurando el navegador
        
    try:
        # Aceptamos las cookies de la página
        time.sleep(3) 
        button = driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()  
        print("Cookies aceptadas.")

    except Exception as e:
        print("Error al encontrar o hacer click en el botón",e)

    try: # Entramos en los links
        time.sleep(2)
        movies = driver.find_element(By.ID, "A54115753").click()
        print ("Hecho")
    except Exception as e:
        print("Error al ejecutar",e)

    try: #Entramos en el panel de características
        time.sleep(2)
        movie_charact = driver.find_element(By.CLASS_NAME, "extra-info__item").click()
        print("Abrimos panel")
    except Exception as e:
        print("Error al pulsar",e)


    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
