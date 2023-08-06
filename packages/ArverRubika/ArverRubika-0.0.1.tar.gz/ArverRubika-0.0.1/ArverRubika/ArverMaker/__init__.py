#pylint:disable=E0401
from ArverRubika.cryptos import cryption
from ArverRubika.servers import get_server
from json import dumps, loads
from urllib3 import PoolManager
from requests import post , get
class makers:
    
    def __init__(self, auth):
        self.auth = auth
        self.crypto = cryption(auth)
        self.http = PoolManager()
        self.server = get_server('api')
        self.req_clients = {
            'web': {
                'app_name': 'Main',
                'app_version': '4.1.7',
                'platform': 'Web',
                'package': 'web.rubika.ir',
                'lang_code': 'fa'
            },
            'android': {
                'app_name': 'Main',
                'app_version': '3.0.9',
                'platform': 'Android',
                'package': 'ir.resaneh1.iptv',
                'lang_code': 'fa'
            }
        }
        del auth

    def method(self, method, data):
        data = {
            'api_version': '5',
            'auth': self.auth,
            'data_enc': self.crypto.encrypt(
                dumps(
                    {
                        'method': method,
                        'input': data,
                        'client': self.req_clients['web']
                    }
                )
            )
        }
        result = self.http.request(
            'POST',
            self.server,
            body = dumps(data).encode(),
            headers = {'Cookie': 'Arver Library'}
        )
        result = loads(self.crypto.decrypt(loads(result.data.decode('utf-8'))['data_enc']))
        if result['status'] == 'OK':
            return result
        elif result['status'] in ['ERROR_GENERIC', 'ERROR_ACTION']:
            if result['status_det'] == 'INVALID_AUTH':
                raise IndexError("Auth Not True .!")
            else:
                pass
    def _upload(self, url, data, headers):
        while True:
            req = post(url=url, data=data, headers=headers)
            if req.status_code != 200:
                "This file cannot be uploaded ! Trying to upload again ..."
                continue
            return req.json()