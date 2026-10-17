from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Switch between different environment files based on the mode by enabling different env files
# .env - production
# .env.local - development
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
# load_dotenv(Path(__file__).resolve().parent.parent / ".env.local")

if getenv("MODE") == "production":
    engine = create_engine(
        getenv("DATABASE_URL")
    )
else:
    CREATE_DATABASE_URL = URL.create(
        drivername=getenv("PG_DRIVER_NAME"),
        database=getenv("PG_DB_NAME"),
        username=getenv("PG_USER"),
        password=getenv("PG_PASSWORD"),
        host=getenv("PG_HOST"),
        port=getenv("PG_PORT")
    )
    engine = create_engine(CREATE_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()