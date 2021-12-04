from configparser import ConfigParser
import asyncio
import requests


class AlpacaParser():

    def __init__(self) -> None:
        try:
            config = ConfigParser()
            config.read_file('config.ini')
        
        except KeyError:
            print(KeyError)
            return

        self.url = config['PAPER_API_URL']
        self.api_key = config['PAPER_API_KEY']
        self.api_secret = config['PAPER_API_SECRET']

    async def get_balance(self):
        req = await requests.get(f"{self.url}/v2/account",headers={"APCA-API-KEY-ID":self.api_key,"APCA-API-SECRET-KEY":self.api_secret})
        result = await req.json()
        return result