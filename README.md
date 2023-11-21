# PROYECTO DE RECONOCIMIENTO DE EMOCIONES DE UNA VIDEO ENTREVISTA

Aplicación desarrollada con Flask por alumos de la Universidad San Sebastián, la cuál consiste en procesar una video entrevista para extraer 30 fotogramas equisdistantes en tiempo entre sí, para luego realizar el análisis de cada una de ellas con los servicios de aws rekognition. Los resultados son almacenados en un excel el cual queda disponible para descarga como respuesta de la app. A continuación, se explica como ejecutar la aplicación.

### Requisitos
 - Python 3.x
 - Pip (instalador de paquetes)
 
### Instalación
1. Clonar repositorio en tu máquina local
    ```bash
    git clone https://github.com/tu-usuario/nombre-del-repositorio.git
    ```
2. Dentro del directorio, ejecutar ejecutar lo siguiente para instalar las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```
3. Dentro de tu proyecto, crea el archivo .env a partir del .env.example y reemplaza `your_access_key`, `your_secret_key`, y `your_region` con tus credenciales de aws Rekognition:
    ```env
    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    AWS_REGION=your_region
    ```

### Ejecución
1. Ejecutar la aplicación Flask:

    ```bash
    python app.py
    ```
2. Abrir Postman o el cliente HTTP que utilices.
3. Realizar la solicitud POST a la ruta `/procesar_video`, pasando dentro del body una variable de key `video` y value el archivo de video a procesar.
4. La respuesta, en caso de ser status 200, es el archivo descargable con los resultados del análisis y los gráficos correspondientes por cada una de las emociones encontradas. 
En postman, es necesario guardar la respuesta para ver el archivo.