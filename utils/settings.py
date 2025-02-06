import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    apikey_bitget: str
    apisec_bitget: str
    apiphrase_bitget: str

settings = Settings(
    apikey_bitget=os.getenv('apikey_bitget'),
    apisec_bitget=os.getenv('apisec_bitget'),
    apiphrase_bitget = os.getenv('apiphrase_bitget')
)