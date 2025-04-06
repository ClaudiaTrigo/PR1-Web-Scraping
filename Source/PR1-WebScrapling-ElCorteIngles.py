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
    # 1. Configurar Selenium con el Webdriver
    service=Service(ChromeDriverManager().install())
    option=webdriver.ChromeOptions()
    # abriremos el navegador en modo incognito
    option.add_argument("--incognito")

    # Deshabilitar banderas que identifican a Selenium
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    # Opcionalmente, podemos usar un User-Agent personalizado esto puede ayudar a 'simular' un navegador real en lugar del de Selenium para que no nos detecte.
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

    # 2. Abrir la página
    driver.get("https://www.elcorteingles.es/cine/accion-y-aventuras/") 

    # Aceptamos las cookies de la página principal  
    try:
        time.sleep(4) 
        button = driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()  
        print("Cookies aceptadas en la página principal.")

    except Exception as e:
        print("Error al encontrar o hacer click en el botón en la página principal",e)

    # 3. Hacer scroll infinito para cargar más películas
    scroll_pause_time = 5  # Segundos a esperar tras cada scroll
    scroll_increment = 800  # Pixeles que avanza el scroll en cada iteración

    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0

    while True:
        # Desplaza el scroll a la posición actual
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)  # Espera que se carguen los nuevos elementos
    
        # Verifica si la altura de la página ha aumentado (nuevos elementos)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            # Se han cargado más elementos, actualizamos la altura y seguimos
            last_height = new_height
    
        # Avanza el scroll
        current_position += scroll_increment

        # Si al avanzar superamos la nueva altura, rompemos el bucle
        if current_position >= new_height:
            print("Llegamos al final del scroll (o no se cargan más elementos).")
            break 
        time.sleep(2)

    # 4. Localizar todas las portadas (WebElements) con clase "js_preview_image"
    try:
        time.sleep(4)
        movie_elements = driver.find_elements(By.CLASS_NAME, "js_preview_image")
        print("Portadas localizadas:", len(movie_elements))
    except Exception as e:
        print("Error al intentar localizar las peliculas:", e)
        movie_elements = []

    # 5. Extraer los enlaces de cada portada
    links_movies = []
    for movie_el in movie_elements:
        try:
            # Subir al <a> contenedor
            parent_anchor = movie_el.find_element(By.XPATH, "./ancestor::a")
            link = parent_anchor.get_attribute("href")
            if link:
                links_movies.append(link)
        except Exception as e:
            print("Error al recopilar un link:", e)

    print(f"Se han recopilado {len(links_movies)} links de películas.")

    # 6. Recorrer cada enlace y extraer titulo + datos del panel
    datos = []
    for link in links_movies:
        try:
            driver.get(link)
            time.sleep(4)

            # Aceptar cookies si vuelven a aparecer
            try:
                driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
                print("Cookies aceptadas p.2.")
            except:
                pass

            record = {} #creamos un diccionario para cada pelicula

            # (A) EXTRAER TÍTULO 
            try:
                title_elem = driver.find_element(By.ID, "product_detail_title").text
                record["Título"] = title_elem
            except:
                record["Título"] = "N/A"

            # (B) EXTRAEMOS PRECIOS 
            try:
                Price = driver.find_element(By.CSS_SELECTOR, ".price-unit--normal.product-detail-price")
                record["Precio de venta"] = Price.text.strip()
            except:
                record["Precio de venta"] = "N/A"

            # (C) Hacer click en “Características”
            try:
                time.sleep(2)
                panel_span = driver.find_element(By.XPATH, "//div[@class='extra-info__item']//span[normalize-space()='Características']").click()
                print("Abrimos panel de características")
                time.sleep(1)
            except Exception as e:
                print("Error al pulsar en el panel de características:", e)

            # (D) EXTRAER el resto de datos del panel

            # 1) Localizar todos los <dt class="titleInfoProduct">
            dt_elements = driver.find_elements(By.CSS_SELECTOR, "dt.titleInfoProduct")

            # 2) Definir las palabras clave que te interesan:
            campos_interes = {
                "Editor": "Editor",
                "Fecha de lanzamiento": "Fecha de lanzamiento",
                "Subtítulos": "Subtítulos",
                "Idioma": "Idioma",
                "Año": "Año",
                "País": "País",
                "Duración": "Duración",
                "Calificación": "Calificación"  
            }

            for dt in dt_elements:
                label_text = dt.text.strip()
    
                # 3) Localizar el <dd> inmediatamente siguiente 
                try:
                    dd_element = dt.find_element(By.XPATH, "./following-sibling::dd[1]")
                    value_text = dd_element.text.strip()
                except:
                    value_text = "N/A"

                # 4) Comprobar si la etiqueta dt coincide con uno de los campos que quieres
                for campo, patron in campos_interes.items():
                # "campo" es la clave con la que guardarás la info en el diccionario
                # "patron" es el texto que esperas (p. ej., "Fecha de lanzamiento")

                    if patron in label_text:
                        record[campo] = value_text
                        break  # Salimos del bucle interno "for campo, patron"

            # (E) Guardar link también, por si lo quieres en el CSV
            record["Link"] = link

            # (F) Añadir el diccionario a la lista de datos
            datos.append(record)   
            
        except Exception as e:
            print(f"Error procesando {link}: {e}")

    # 7. Convertir la lista de diccionarios en un DataFrame y a CSV
    df = pd.DataFrame(datos)
    df.to_csv("Peliculas_Acción_Aventuras_Corte_Inglés_abril_2025_bruto.csv", index=False, encoding='utf-8-sig')
    print("Datos guardados en 'Peliculas_Acción_Aventuras_Corte_Inglés_abril_2025_bruto.csv'")

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    main()