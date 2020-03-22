
import os
from dotenv import load_dotenv
from alpaca_trade_api import REST

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") 
KEY_ID = os.getenv("KEY_ID")
BASE_URL = os.getenv("BASE_URL")

class AlpacaSocket(REST): 
    def __init__(self): 
        super().__init__(
            key_id=KEY_ID,
            secret_key=SECRET_KEY,
            base_url=BASE_URL
        )