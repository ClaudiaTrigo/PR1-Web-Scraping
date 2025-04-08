# Descripción
Este proyecto se ha desarrollado bajo el contexto de la asignatura **Tipología y ciclo de vida de los datos**, perteneciente al Máster en Ciencia de Datos de la **Universitat Oberta de Catalunya (UOC)**. En él, se han aplicado técnicas de **web scraping** con el lenguaje de programación **Python**, utilizando la librería **Selenium** para extraer información de la sección de Cine (género “Acción y Aventuras”) de la web de **El Corte Inglés**.

# Miembros del equipo
El trabajo ha sido realizado por:
- **Claudia Sánchez Arnau**
- **Claudia Trigo Joaquin**

# Ficheros del código fuente

1. **PR1-WebScraping-ElCorteIngles.py**  
   Contiene el código Python que realiza el scraping:
   - Inicia la navegación en la página de El Corte Inglés.
   - Efectúa un *scroll* infinito para cargar todas las películas.
   - Recorre cada enlace para extraer datos (título, precio, características, etc.).
   - Exporta la información en un fichero CSV.

2. **requirements.txt**  
   Lista de librerías necesarias para reproducir el entorno de ejecución.

3. **Peliculas_Acción_Aventuras_Corte_Inglés_abril_2025_bruto.csv**  
   Dataset resultante, que recoge toda la información recopilada: título de las películas, precio, editor, fecha de lanzamiento, subtítulos, idioma, etc.

# Enlace al dataset publicado en Zenodo
   https://doi.org/10.5281/zenodo.15169026

# Instrucciones de ejecución
```bash
# 1. Clona o descarga este repositorio
git clone https://github.com/ClaudiaTrigo/PR1-Web-Scrappling.git

# 3. Instala las dependencias del archivo requirements.txt
pip install -r requirements.txt

# 4. Ejecuta el script principal de scraping
python PR1-WebScrapling-ElCorteIngles.py

# Al finalizar, se generará el fichero CSV con los datos extraídos.

