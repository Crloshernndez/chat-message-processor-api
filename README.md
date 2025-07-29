# chat-message-processor-api
Message Processing API

## Ejecución con Docker
Para ejecutar la aplicación usando Docker y Docker Compose:

1.  Asegúrate de tener Docker Desktop (o Docker Engine y Docker Compose) instalado en tu sistema.
2.  Navega a la raíz del proyecto en tu terminal.
3.  Para ver todos los comandos disponibles:
    ```bash
    make help
    ```
4.  Para construir la imagen Docker y levantar los servicios:
    ```bash
    make start
    ```
5.  La API estará disponible en `http://localhost:8000`.
6.  La documentación interactiva (Swagger UI) estará en `http://localhost:8000/docs`.
7.  Para detener los contenedores:
    ```bash
    make stop
    ```
8.   Para ejecutar las pruebas unitarias y de integración:
    ```bash
    make test
    ```
9.   Para ejecutar el linter (Flake8):
    ```bash
    make lint
    ```
10.  Para limpiar el entorno (eliminar entorno virtual, archivos de base de datos, caché de Docker, etc.):
    ```bash
    make clean
    ```


## Ejecución con Docker
Si prefieres ejecutar la aplicación directamente en tu máquina local:

1.  Asegúrate de tener Python 3.10+ instalado.
2.  Navega a la raíz del proyecto en tu terminal.
3.  Para crear el entorno virtual e instalar las dependencias:
    ```bash
    make install-deps
    ```
    Después de ejecutar esto, deberás activar tu entorno virtual manualmente y luego instalar las dependencias:
    ```bash
    # Para Linux/macOS
    source venv/bin/activate
    pip install -r requirements.txt
    # Para Windows
    # .\venv\Scripts\activate
    # pip install -r requirements.txt
    ```
4.  Para ejecutar la aplicación localmente:
    ```bash
    make run-local
    ```
    Después de ejecutar esto, deberás activar tu entorno virtual y luego iniciar Uvicorn:
    ```bash
    # Para Linux/macOS
    source venv/bin/activate
    uvicorn main:app --reload
    # Para Windows
    # .\venv\Scripts\activate
    # uvicorn main:app --reload
    ```