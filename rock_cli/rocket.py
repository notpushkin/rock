import hashlib
import time
import uuid
import json as json_

import requests

API_VERSION = "5"

class Rocket:
    def __init__(self, device_id=None, token=None, user_agent=None):
        self.token = token
        self.device_id = device_id or self.generate_id()
        self.user_agent = user_agent or \
                "RocketScience/%s (ale@songbee.net)" % API_VERSION

    @staticmethod
    def generate_id(namespace="SCIENCE"):
        return "%s_%s" % (namespace, hex(uuid.getnode()).replace("0x", ""))

    def request(self, method, url, headers=None, json=None, **kw):
        headers = headers or {}
        json = json or {}

        if not url.startswith(("http://", "https://")):
                url = "https://rocketbank.ru/api/v5/" + url

        headers['x-device-id'] = self.device_id
        headers['User-agent'] = self.user_agent

        now = int(time.time())
        headers['x-sig'] = hashlib.md5((\
                "0Jk211uvxyyYAFcSSsBK3+etfkDPKMz6asDqrzr+f7c=_" + \
                str(int(now)) + "_dossantos").encode()).hexdigest()
        headers['x-time'] = str(now)
        headers['content-type'] = "application/json"

        if self.token:
            json['token'] = self.token

        r = requests.request(method, url, data=json_.dumps(json), headers=headers, **kw)
        try:
            resp = r.json()['response']
        except:
            resp = {
                'description': "Unknown error",
                'status': r.status_code,
                'code': "UNKNOWN"
            }

        if r.status_code != requests.codes.ok:
            raise RocketException(
                description=resp['description'],
                status=resp['status'],
                code=resp['code'])

        return r

    def head(self, *a, **kw):     return self.request("HEAD", *a, **kw)
    def get(self, *a, **kw):        return self.request("GET", *a, **kw)
    def post(self, *a, **kw):     return self.request("POST", *a, **kw)
    def put(self, *a, **kw):        return self.request("PUT", *a, **kw)
    def patch(self, *a, **kw):    return self.request("PATCH", *a, **kw)
    def delete(self, *a, **kw): return self.request("DELETE", *a, **kw)

    def register(self, phone):
        r = self.post(
            "/devices/register",
            json={'phone': phone})
        id = r.json()['sms_verification']['id']
        return RocketSmsVerification(id, self)

    def login(self, email, password):
        """
        email == привязанный email
        password == "рокеткод" / код, вводимый при открытии
        """
        r = self.get(
            "/login",
            json={
                'email': email,
                'password': password
            })
        j = r.json()

        if 'token' in j:
            self.email = email
            self.password = password
            self.token = j['token']

        return j

    def tariffs(self):
        r = self.get("https://rocketbank.ru/api/v4/tariffs")
        for j in r.json():
            yield RocketTariff(j)

    @property
    def balance(self):
            return self._feed.balance

    @property
    def operations(self):
        return self._feed.operations


class RocketException(Exception):
    def __init__(self, description, status, code):
        self.description = description
        self.status = status
        self.code = code

    def __str__(self):
        return self.description


class RocketSmsVerification:
    def __init__(self, id, rocket):
        self.id = id
        self.rocket = rocket

    def verify(self, code):
        r = self.rocket.patch(
            "/sms_verifications/%s/verify" % self.id,
            json={'code': code})
        j = r.json()

        if 'token' in j:
            self.rocket.token = j['token']

        return j

    def __repr__(self):
        return "<RocketSmsVerification '%s'>" % self.id
