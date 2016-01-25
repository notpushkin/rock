import hashlib
import time
import uuid
import json as json_

from arequests import API
from requests.auth import AuthBase

API_VERSION = "5"

class Rocket(API):
    base_url = "https://rocketbank.ru/api/v5"

    def __init__(self, device_id=None, token=None, user_agent=None):
        super(Rocket, self).__init__()

        self.session.headers.update({
            'X-Device-ID': device_id or self.generate_id(),
            'User-agent': user_agent or \
                    "RocketScience/%s (ale@songbee.net)" % API_VERSION,
            # 'Content-type': "application/json",
        })
        if token is not None:
            self.session.auth = RocketAuth(token)


    @staticmethod
    def generate_id(namespace="SCIENCE"):
        return "%s_%s" % (namespace, hex(uuid.getnode()).replace("0x", ""))

    def set_token(self, token):
        self.session.auth = RocketAuth(token)


class RocketAuth(AuthBase):
    def __init__(self, token=None):
        self.token = token

    def __call__(self, r):
        # modify and return the request
        if self.token is not None:
            j = {}
            if r.body is not None:
                try:
                    j = json_.loads(r.body)
                except ValueError:
                    pass # or raise?
            j['token'] = self.token
            r.body = json_.dumps(j)
            r.headers['Content-type'] = "application/json"

        now = int(time.time())
        r.headers['x-sig'] = hashlib.md5((\
                "0Jk211uvxyyYAFcSSsBK3+etfkDPKMz6asDqrzr+f7c=_" + \
                str(int(now)) + "_dossantos").encode()).hexdigest()
        r.headers['x-time'] = str(now)
        return r
