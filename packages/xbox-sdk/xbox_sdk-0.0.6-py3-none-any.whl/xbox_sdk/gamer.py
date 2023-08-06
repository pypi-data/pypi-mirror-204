from xboxapi.gamer import Gamer as XboxAPIGamer
from xbox_sdk.client import Client

class Gamer:
    def __init__(self, gamertag=None, client=None, xuid=None):
        self.__client = client
        self.__gamer = XboxAPIGamer(gamertag=gamertag, client=client, xuid=xuid)

    def fetch_xuid(self):
        return self.__gamer.fetch_xuid()

    def get(self, method=None, term=None):
        return self.__gamer.get(method=method, term=term)

    def parse_endpoints_secondary(self, method=None, term=None):
        return self.__gamer.parse_endpoints_secondary(method=method, term=term)

    def post_activity(self, message=None):
        return self.__gamer.post_activity(message=message)

    def send_message(self, message=None, xuids=None):
        return self.__gamer.send_message(message=message, xuids=xuids)
