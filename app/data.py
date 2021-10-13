"""
Labs DS Data Engineer Role
- Database Interface
- Visualization Interface
"""
import os

from dotenv import load_dotenv


class Data:
    load_dotenv()
    db_url = os.getenv("DB_URL")
