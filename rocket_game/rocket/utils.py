from pygost import gost28147
import secrets

def PSP(number):
    key = secrets.token_bytes(32)
    sbox = "id-Gost28147-89-CryptoPro-A-ParamSet"
    random_bytes = gost28147.encrypt(key=key, ns=(1, 1), sbox=sbox)
    return (random_bytes[1] % number) + 1