import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    apikey_bitget: str
    apisec_bitget: str
    apiphrase_bitget: str
    dropbox_key:str
    dropbox_secret:str
    dropbox_refresh:str
settings = Settings(
    apikey_bitget=os.getenv('apikey_bitget'),
    apisec_bitget=os.getenv('apisec_bitget'),
    apiphrase_bitget = os.getenv('apiphrase_bitget'),
    dropbox_key=os.getenv('dropbox_key'),
    dropbox_secret=os.getenv('dropbox_secret'),
    dropbox_refresh=os.getenv('dropbox_refresh')
)