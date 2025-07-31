from fastapi import FastAPI
from app.infrastructure.persistence.database import create_db_tables
from app.infrastructure.routes.auth_routes import router as auth_router
from app.infrastructure.routes.user_routes import router as user_router
from app.infrastructure.routes.message_router import router as message_router

app = FastAPI(
    title="API de Procesamiento de Mensajes de Chat",
    description="Una API RESTful simple para procesar y\
        almacenar mensajes de chat.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """
    Function that runs when the application starts.
    Creates the database tables if they don't exist.
    """
    create_db_tables()
    print("Database and tables initialized.")


app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(message_router, prefix="/api")


@app.get("/")
async def root():
    """
    Root endpoint to check the status of the API.
    """
    return {"message": "Chat Message Processing API is working properly!"}
