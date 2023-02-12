# PR_1_MovieScrapper

Autores:
- Clara Matilde Roca de la Concha
- Victor Ayala Sánchez

El presente repositorio contiene los ficheros que corresponden al proyecto de la primer práctica.
A continuación se describe la estructura del mismo:

### Source
En este subdirectorio encontraremos los ficheros correspondientes al desarrollo realizado para la captura de datos y el output correspondiente, sin ningún tipo de limpieza.

- Fichero PR1_spider.ipynb, contiene la spyder programada cuyo output es un fichero json.
- PR1_spider.py, es un fichero plano de python con la misma spyder desarrollada en el notebook.
- data_wiki.json, contiene toda la información capturada por la spi¡yder. Este fichero debe ser limpiado para obtener los datos.

### Dataset
En este subdirectorio se tiene los ficheros que componen el conjunto de datos.

- df_castData.csv, contiene la información del reparto: actores y actrices que protagonizaron las diferentes películas.
- df_metamovies.csv, contiene información extra de las películas: dirección, guión, presupuesto, etc.
- df_movies, tiene la información sobre las películas nominadas a los premios de la academia.

El conjunto de datos también se encuentra publicado en el siguiente enlace de [Zenodo](https://doi.org/10.5281/zenodo.7328744)

### Directorio Raíz
- DataClean.ipynb, se trata de un notebook donde se procesa el json del directorio Source y se transforman los datos en tres tablas que conforman el conjunto de datos.
- memoria.pdf, contiene toda la documentación del proyecto.
- requeriments.txt, con las librerías necesarias para ejectuar el código del proyecto.
