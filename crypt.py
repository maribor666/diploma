from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random
import base64
import hashlib
import os

def main():
    # setup()
    data = b'12 43 42 46 af'
    print('data')
    print(data)
    key, data = send_data_to_dron(data)
    receive_data(key, data)

class AESCipher:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        print(len(key))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

def receive_data(key, data):
    private_key = RSA.import_key(open("./keys/private1.pem").read())
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher = PKCS1_v1_5.new(private_key)
    aes_key = cipher.decrypt(key, sentinel)
    print("dec AES key:", aes_key)

    cipher = AESCipher(aes_key)
    aes_key = b'[\x1e\x1erP\x02S\xa9k\xe3\x10\xad\xb71c<'
    decrypted = cipher.decrypt(data, aes_key)
    print('decrypted')
    print(decrypted)
    return decrypted

def send_data_to_dron(data):
    key = os.urandom(16)
    print("gen AES key:", key)
    cipher = AESCipher(key)
    ciphertext = cipher.encrypt(data, key)

    rsa_public1 = RSA.import_key(open("./keys/public1.pem").read())
    cipher = PKCS1_v1_5.new(rsa_public1)
    ecnrypted_aes_key = cipher.encrypt(key)
    return ecnrypted_aes_key, ciphertext

def setup():
    key1 = RSA.generate(2048)
    private_key1 = key1.export_key()
    fileout = open("./keys/private1.pem", mode="wb+")
    fileout.write(private_key1)
    public_key1 = key1.publickey().export_key()
    file_out = open("./keys/public1.pem", "wb+")
    file_out.write(public_key1)

    key2 = RSA.generate(2048)
    private_key2 = key2.export_key()
    fileout = open("./keys/private2.pem", mode="wb+")
    fileout.write(private_key2)
    public_key2 = key2.publickey().export_key()
    file_out = open("./keys/public2.pem", "wb+")
    file_out.write(public_key2)

    send_private("./keys/private1.pem", to='dron')
    send_private("./keys/private2.pem", to='operator')
    send_public("./keys/public1.pem", to='dron')
    send_public("./keys/public2.pem", to='operator')

def send_private(keyfile_path, to='dron'):
    pass

def send_public(keyfile_path, to='dron'):
    pass

if __name__ == '__main__':
    main()