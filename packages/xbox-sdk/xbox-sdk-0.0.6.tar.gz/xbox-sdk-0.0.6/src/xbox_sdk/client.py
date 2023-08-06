"""
https://github.com/mKeRix/xboxapi-python
"""

from xboxapi.client import Client as XboxAPIClient
from xbox_sdk.timeout import Timer


class Client:
    def __init__(self, api_key=None, timeout=3):
        if api_key is None:
            self.__client = self.__new_client()
        else:
            self.__client = XboxAPIClient(api_key=api_key)
        self.__client.timeout = timeout
        self.__timer = Timer(self.__client)
        self.reset_timer = self.__timer.reset_timer
        self.limit = self.__timer.limit
        self.remaining = self.__timer.remaining

    def __get_keys(self):
        from pathlib import Path
        import os
        import json
        key_file = Path(os.environ.get("KEY")) / Path("api_keys.json")
        with open(key_file, "r") as r:
            data = json.load(r)
            return data['https://xapi.us/']['accounts']

    def __new_client(self):
        accounts = self.__get_keys()
        for account in accounts:
            if account['username'] == 'ensue':
                return XboxAPIClient(api_key=account['key'])

    def set_timeout(self, seconds):
        self.__client.timeout = seconds

    def set_api_key(self, key):
        self.__client.api_key = key

    def set_continuation_token(self, token):
        self.__client.continuation_token = token

    def gamer(self, gamertag, xuid=None):
        return Gamer(gamertag=gamertag, client=self, xuid=xuid)

    def cache_calls_remaining(self):
        return {'X-RateLimit-Reset': self.reset_timer,
                'X-RateLimit-Limit': self.limit,
                'X-RateLimit-Remaining': self.remaining}

    def calls_remaining(self):
        self.__timer = Timer(self.__client)
        self.reset_timer = self.__timer.reset_timer
        self.limit = self.__timer.limit
        self.remaining = self.__timer.remaining
        return self.cache_calls_remaining()

    def api_get(self, method):
        self.decrement()
        return self.__client.api_get(method)

    def api_post(self, method,  body=None):
        self.decrement()
        return self.__client.api_post(method, body)

    def xboxapi_response_error(self, response):
        return self.__client.xboxapi_response_error(response)

    def decrement(self):
        if self.remaining <= 0:
            self.__timer.start_timeout()
        if self.remaining > 10 and self.remaining % 50 == 0 or self.remaining < 10:
            rate = self.__client.calls_remaining()
            self.reset_timer = int(rate['X-RateLimit-Reset'])
            self.remaining = int(rate['X-RateLimit-Remaining']) - 1
        self.remaining -= 1
