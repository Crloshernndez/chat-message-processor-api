import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./instance/chat_messages.db"
    )

instance_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
if instance_dir and not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# connect_args={"check_same_thread": False} is needed for SQLite
#  to allow multiple threads
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

# Create a SessionLocal class to get a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create a declarative base for defining ORM models
Base = declarative_base()


# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield
    finally:
        db.close()


# Function to create database tables
def create_db_tables():
    Base.metadata.create_all(bind=engine)
