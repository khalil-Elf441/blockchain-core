from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
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
        except(IOError,IndexError) as e:  
            print("Saving wallet keys failed...")
            print(e)
        finally:
            print(" save_keys finsh !")



    def load_keys(self) -> None:
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except(IOError,IndexError) as e: 
            print("loading wallet keys failed...")
            print(e)
        finally:
            print(" load_keys finsh !")


    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'),
        binascii.hexlify(public_key.export_key(format='DER')).decode('ascii'))

    def sign_transaction(self, t_from, t_to, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        tx_hash = SHA512.new((str(t_from)+str(t_to)+str(amount)).encode('utf8'))
        signature = signer.sign(tx_hash)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.t_from))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA512.new((str(transaction.t_from) + str(transaction.t_to) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
        