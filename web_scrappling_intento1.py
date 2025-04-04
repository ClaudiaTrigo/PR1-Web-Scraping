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
    # abriremos el navegador en modo incognito
    option.add_argument("--incognito")

    # Deshabilitar banderas que identifican a Selenium
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    # Opcionalmente, podemos usar un User-Agent personalizado
    # (esto puede ayudar a 'simular' un navegador real en lugar del de Selenium)
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/99.0.4844.51 Safari/537.36")

    driver= Chrome(service=service, options=option)

    # Ejecutar script para ocultar la propiedad webdriver en tiempo de ejecución
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    # Configurando el navegador
    driver.get("https://www.elcorteingles.es/cine/accion-y-aventuras/") 
        
    try:
        # Aceptamos las cookies de la página principal
        time.sleep(4) 
        button = driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()  
        print("Cookies aceptadas.")

    except Exception as e:
        print("Error al encontrar o hacer click en el botón",e)

    #Buscar todas las portadas de peliculas
    movie_elements = []
    try: 
        # Entramos en los links y localizamos las peliculas
        time.sleep(4)
        movie_elements = driver.find_elements(By.CLASS_NAME, "js_preview_image")
        print ("Portadas localizadas")
    except Exception as e:
        print("Error al intentar localizar las peliculas",e)
    
    links_movies = [] # Extraer los enlaces de cada portada para navegar después
    for movie_el in movie_elements:
        try:
            # Vamos a su elemento <a> donde encontraremos los URL
            parent_anchor = movie_el.find_element(By.XPATH, "./ancestor::a")
            link = parent_anchor.get_attribute("href")
            if link:
                links_movies.append(link)
            print("Estamos recopilando los links")
        except Exception as e:
            pass  
            print("Error al recopilar los links",e)
        
    print(f"Se han recopilado {len(links_movies)} links de películas.")
    
    datos = [] #Lista donde guardaremos la info de todas las pelis

    for link in links_movies:
         
        try:
            driver.get(link)
            # Aceptamos las cookies de la página
            time.sleep(4) 
            try:
                button2 = driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()  
                print("Cookies aceptadas p.2.")

            except Exception as e:
                pass 
                
            try: #Entramos en el panel de características
                time.sleep(2)
                movie_charact = driver.find_element(By.CLASS_NAME, "extra-info__item").click()
                print("Abrimos panel de características")
                time.sleep(1)
            except Exception as e:
                print("Error al pulsar en el panel de características",e)

            # Ahora pasamos a la extracción de datos: 

            try: # Ahora haremos la extracción de los datos del titulo
                title = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[5]/div/dd/div').text
            except:
                title = "N/A"
            
            try: # Ahora haremos la extracción de la fecha de lanzamiento
                launch_date = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[3]/div/dd/div').text
            except:
                launch_date = "N/A"

            try: # Ahora haremos la extracción de los datos del editor
                editor = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[1]/div/dd/div').text
            except:
                editor = "N/A"

            try: # Ahora haremos la extracción de los datos del país
                country = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[9]/div[3]/dd/div').text
            except:
                country = "N/A"

            try: # Ahora haremos la extracción de la duracion
                duration = driver.find_element(By.XPATH, '///*[@id="modal"]/div/div/div/div/div/dl[9]/div[4]/dd/div').text
            except:
                duration = "N/A"

            try: # Ahora haremos la extracción de la edad minima
                age = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[9]/div[5]/dd/div').text
            except:
                age = "N/A"

            try: # Ahora haremos la extracción de año de producción
                filming_year = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[9]/div[2]/dd/div').text
            except:
                filming_year = "N/A"

            try: #Ahora pondremos los subtitulos
                subtitles = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div/div/dl[8]/div[3]/dd')
            except:
                subtitles = "N/A"

            datos.append({
            "Titulo": title,
            "Link": link,
            "Data de lancamento": launch_date,
            "Editor": editor,
            "País": country,
            "Duracion": duration,
            "Edad mínima": age,
            "Año de grabación": filming_year,
            "Subtitulos": subtitles
            })
        
        except Exception as e:
            print("Error procesando {link}:{e}")


    # Convertir la lista de diccionarios en un DataFrame y guardarlo a CSV
    df = pd.DataFrame(datos)
    df.to_csv("peliculas.csv", index=False, encoding='utf-8-sig')
    print("Datos guardados en 'peliculas.csv'")

    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
