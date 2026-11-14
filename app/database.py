# -----------------------------------------
# Section 1: Import required libraries
# -----------------------------------------

import os
from pathlib import Path

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL


# -----------------------------------------
# Section 2: Load environment variables
# -----------------------------------------

# Get the location of this app folder
BASE_DIR = Path(__file__).resolve().parent

# Load database details from app/.env
load_dotenv(BASE_DIR / ".env")


# -----------------------------------------
# Section 3: Create SQLAlchemy object
# -----------------------------------------

# This object is used for ORM operations
db = SQLAlchemy()


# -----------------------------------------
# Section 4: Read database configuration
# -----------------------------------------

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# -----------------------------------------
# Section 5: Build database URL
# -----------------------------------------

# URL.create safely handles special characters
# in the database password

DATABASE_URL = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)
