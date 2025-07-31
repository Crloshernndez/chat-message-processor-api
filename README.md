# chat-message-processor-api
Message Processing API

## Descripción
La API chat-message-processor es una solución de backend robusta y escalable diseñada para gestionar la creación, el almacenamiento y la recuperación de mensajes de chat. Su arquitectura, basada en principios de clean architecture, garantiza la separación de responsabilidades, facilitando su mantenimiento y expansión.

Las funcionalidades clave de esta API incluyen:

1.  Gestión de Usuarios y Autenticación: Un sistema seguro para el registro de nuevos usuarios y la autenticación mediante tokens JWT (JSON Web Token), protegiendo así los endpoints sensibles de la API.
   
2.  Procesamiento y Almacenamiento de Mensajes: Permite la creación de nuevos mensajes de chat, aplicando validaciones de datos y un proceso de enriquecimiento que agrega metadatos relevantes como el conteo de palabras y caracteres.
   
3.  Recuperación de Datos Flexible: Ofrece endpoints para consultar mensajes individuales, así como recuperar colecciones de mensajes por sesión, con opciones de paginación y filtrado para una gestión eficiente de grandes volúmenes de datos.
   
4.  Manejo de Errores Uniforme: Un decorador personalizado se encarga de estandarizar la forma en que se manejan las excepciones de negocio y los errores del sistema, garantizando respuestas consistentes y descriptivas para el cliente.

Desarrollada con FastAPI, esta aplicación está optimizada para el alto rendimiento y la fácil integración, y se entrega con una configuración de Docker completa para un despliegue rápido y consistente en cualquier entorno.

## Configuracion de la api
### Ejecución con Docker
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


### Ejecución sin Docker
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

## Cómo Ejecutar las Pruebas:
### Herramienta utilizada
pytest: Framework de testing para Python.

Puedes ejecutar todas las pruebas con un solo comando utilizando el Makefile del proyecto:

    make tests

Este comando ejecutará automáticamente todas las pruebas en el directorio tests/ dentro de tu contenedor de Docker.

Tambien puedes ver la covertura de los test en el codigo el Makefile del proyecto:

    make coverage


## Documentacion de la api
La documentación completa e interactiva de la API está disponible en Swagger UI cuando la aplicación está en ejecución. A continuación, se presenta un resumen de los endpoints principales.

### Usuarios

    POST /api/users/register

    
Registra un nuevo usuario en el sistema. Valida las credenciales, hashea la contraseña y guarda el usuario en la base de datos.

Cuerpo de la Solicitud (JSON):
    1. email (string, requerido): La dirección de correo electrónico única del usuario.
    2. username (string, requerido): El username de usuario único.
    3. password (string, requerido): La contraseña en texto plano (será hasheada antes de almacenarse).
                                    contraseña debe ser mayor a 6 digitos, tener un caracter mayuscula y uno minuscula.

Respuesta

    {
        "status": "success",
        "data": {
            "email": "empanada2@example.com",
            "username": "empanada2"
        }
    }


### Autenticación


    POST /api/auth/token


Permite a un usuario iniciar sesión y obtener un token de acceso JWT (JSON Web Token) para autenticarse en rutas protegidas.

Cuerpo de la Solicitud (JSON):
    1. email (string, requerido): El correo electrónico del usuario.
    2. password (string, requerido): La contraseña en texto plano del usuario.

Respuesta


    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOGlkNGZhZS03ZGVjLTExZDAtYTc2NS0wMGEwYzkxZTZiZjYiLCJleHAiOjE2NzgwNTI0MDB9.some_signature_here",
        "token_type": "bearer"
    }



### Mensajes


    POST /api/messages/


Crea un nuevo mensaje de chat en el sistema, aplicando validaciones y procesamiento de metadatos. Requiere autenticación.

Cuerpo de la Solicitud (JSON):
    1. session_id (string, requerido): Identificador único de la sesión de chat (formato UUID).
    2. content (string, requerido): Contenido del mensaje. El contenido inapropiado será filtrado.
    3. timestamp (string, requerido): Marca de tiempo de cuándo fue enviado el mensaje
    4. sender (string, requerido): Remitente del mensaje ("user" o "system").

Encabezados (para autenticación):
    Authorization: Bearer <tu_token_jwt>

Respuesta


    {
        "status": "success",
        "data": {
            "message_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "session_id": "session-abcdef",
            "content": "Hola, ¿cómo puedo ayudarte hoy?",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user",
            "metadata": {
                "word_count": 6,
                "character_count": 28,
                "processed_at": "2023-06-15T14:30:05Z"
            }
        }
    }




    POST /api/messages/detail/{message_id}


Recupera un mensaje de chat específico utilizando su identificador único. Requiere autenticación.

Parámetros de Ruta:
    1. message_id (string, requerido): El ID único del mensaje (formato UUID).

Encabezados (para autenticación):
    Authorization: Bearer <tu_token_jwt>

Respuesta


    {
        "status": "success",
        "data": {
            "message_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "session_id": "session-abcdef",
            "content": "Hola, ¿cómo puedo ayudarte hoy?",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user",
            "metadata": {
                "word_count": 6,
                "character_count": 28,
                "processed_at": "2023-06-15T14:30:05Z"
            }
        }
    }


    POST /api/messages/{session_id}


Recupera todos los mensajes asociados a un ID de sesión específico, con soporte para paginación y filtrado por remitente. Requiere autenticación.

Parámetros de Ruta:
    1. session_id (string, requerido): El ID único de la sesión de chat (formato UUID).

Parámetros de Consulta (Query Parameters):
    1. limit (entero, opcional): Número máximo de mensajes a devolver. Debe ser un valor entero positivo (mínimo 1).
    2. offset (entero, opcional): Número de mensajes a omitir desde el inicio de la lista. Debe ser un valor entero no negativo (mínimo 0).
    3. sender (string, opcional): Filtra mensajes por el remitente. Valores permitidos: "user" o "system".

Encabezados (para autenticación):
    Authorization: Bearer <tu_token_jwt>

Respuesta


    {
        "messages": [
            {
                "id": "4b0e9f1a-3d2c-4e5f-8a9b-0123456789de",
                "session_id": "c7f8e9d0-a1b2-4c3d-9e0f-1234567890ab",
                "content": "Hola, ¿cómo puedo ayudarte hoy ***?",
                "timestamp": "2023-06-15T14:30:00",
                "sender": "system",
                "metadata": {
                    "word_count": 6,
                    "character_count": 30,
                    "processed_at": "2025-07-30T20:56:38.616004"
                }
            }
        ],
        "pagination": {
            "total": 1,
            "limit": 50,
            "offset": 0,
            "has_next": false,
            "has_previous": false
        }
    }

