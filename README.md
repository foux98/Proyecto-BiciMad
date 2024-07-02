# Proyecto BiciMAD y Universidades



El objetivo de este proyecto es encontrar las estaciones de BiciMAD más cercanas a las universidades en Madrid. Utilizando datos de BiciMAD y datos de universidades, se calcula la distancia entre cada universidad y la estación de BiciMAD más cercana, y se visualizan los resultados en un mapa.


1. **Requisitos**
Para ejecutar este proyecto, necesitas tener instalados los siguientes paquetes de Python:

pandas
requests
ast
numpy
shapely
geopandas
argparse
fuzzywuzzy
folium


2. **Cargar y Limpiar Datos de BiciMAD**

**Cargar CSV de BiciMAD**: Se carga el archivo CSV que contiene las estaciones de BiciMAD.

**Desglosar la columna de coordenadas:** Se separan las coordenadas en latitud y longitud.

**Renombrar y limpiar columnas**: Se renombran las columnas para mayor claridad y se eliminan las columnas innecesarias.


3. **Cargar y Limpiar Datos de Universidades**

**Obtener y Normalizar Datos**: Se obtienen los datos de las universidades desde una API y se normalizan para crear un DataFrame de pandas.

**Limpiar columnas**: Se eliminan las columnas innecesarias y se renombran para mayor claridad.

4. **Calcular Distancias**

**Funciones de Conversión y Distancia**: Se definen funciones para convertir coordenadas y calcular distancias entre puntos.

**Encontrar Estación de BiciMAD más cercana**: Se calculan las estaciones de BiciMAD más cercanas para cada universidad y se combinan los datos en un DataFrame.

5. **Paso 4: Guardar y Visualizar**

**Guardar en CSV**: Se guarda el DataFrame combinado en un archivo CSV.

**Crear Mapa con Folium**: Se crea un mapa interactivo que muestra las universidades y las estaciones de BiciMAD más cercanas.

6. **Uso del Script con Argumentos**

Buscar Paradas Cercanas: Se implementa un script que permite buscar la estación de BiciMAD más cercana a una universidad específica utilizando argumentos desde la línea de comandos.


# Conclusiones

Utilizando Python y bibliotecas específicas, logramos limpiar y manipular datos, calcular distancias geográficas, y crear visualizaciones interactivas que facilitan la interpretación de los resultados. 


