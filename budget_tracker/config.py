
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(BASE_DIR / ".env")

DEFAULT_DB = f"sqlite:///{BASE_DIR / 'budget.db'}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

