from Crypto import PublicKey
from Crypto.PublicKey import RSA
import Crypto.Random 
import binascii

class Wallet:
    def __init__(self) -> None:
        self.private_key = None
        self.public_key = None
    
    def create_keys(self) -> None:
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key


    def save_keys(self):
        try:
            with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
        except(IOError,IndexError): 
            print("Saving wallet keys failed...")



    def load_keys(self) -> None:
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except(IOError,IndexError): 
            print("loading wallet keys failed...")


    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'),binascii.hexlify(public_key.export_key(format='DER')).decode('ascii'))