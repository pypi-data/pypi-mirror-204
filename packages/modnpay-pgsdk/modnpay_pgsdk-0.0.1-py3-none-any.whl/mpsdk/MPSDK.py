import base64
import binascii
import json
import os

import requests
import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class MPSDK:

    def __init__(self, request, public_key):
        self.public_key = public_key
        self.requestParams = request.get_json()
        self.byte_xid = os.urandom(16)
        self.xid = binascii.hexlify(self.byte_xid)
        self.iv = self.xid[0:16]

    def order(self):
        e = self.encrypt(json.dumps(self.requestParams))
        k = base64.b64encode(rsa.encrypt(self.xid, self.public_key)).decode('utf-8')

        datas = {
            "mid": self.requestParams['merchantId'],
            'e': e,
            'k': k
        }

        url = "https://dpg.modnpay.kr/api/v1/payments/order"
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        response = requests.post(url, json=datas, headers=headers)

        return response.json()

    def refund(self):
        refundParam = {
            'merchantId': self.requestParams['merchantId'],
            'traceNum': self.requestParams['tid'],
            'refundAmount': self.requestParams['refundAmount']
        }

        e = self.encrypt(json.dumps(refundParam))
        k = base64.b64encode(rsa.encrypt(self.xid, self.public_key)).decode('utf-8')

        datas = {
            "mid": self.requestParams['merchantId'],
            'e': e,
            'k': k
        }

        url = "https://dpg.modnpay.kr/api/v1/payments/refund"
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        response = requests.post(url, json=datas, headers=headers)

        return response.json()

    def encrypt(self, raw):
        cipher = AES.new(self.xid, AES.MODE_CBC, self.iv)
        return bytes.decode(base64.b64encode(cipher.encrypt(pad(raw.encode(), AES.block_size))))

    def decrypt(self, enc):
        cipher = AES.new(self.xid, AES.MODE_CBC, self.iv)
        return bytes.decode(unpad(cipher.decrypt(base64.b64decode(enc)), AES.block_size))
