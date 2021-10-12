import os
import pandas as pd
from dotenv import load_dotenv
class Data:
    load_dotenv()
    db_url = os.getenv("DB_URL")
      