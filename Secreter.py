from cryptography.fernet import Fernet as fr
from cryptography.hazmat.backends import default_backend as df
from  cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as pbk
import os
import random
import base64

def make_key(salt, maspas):
    enpas = maspas.encode()
    pb = pbk(algorithm=hashes.SHA3_512(), length=32, salt=salt, iterations=100000, backend=df())
    return base64.urlsafe_b64encode(pb.derive(enpas))


def encrypt_data(data, key):
    f = fr(key)
    en_data = data.encode()
    return f.encrypt(en_data)


def decrypt_data(data_en, key):
    f = fr(key)
    data = f.decrypt(data_en)
    return data.decode()


#test
#dataa = "lfaflfaf"
#pas= "1234567890"
#salt = os.urandom(random.randint(0, 182))
#key = make_key(salt, pas)
#datae = encrypt_data(dataa, key)
#print(datae)
#key2 = make_key(salt, pas)
#d=decrypt_data(datae, key2)
#print(d)