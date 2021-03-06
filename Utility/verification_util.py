import hashlib
from Utility.hash_util import Hash_util
from wallet import Wallet

class Verification_util:

    @staticmethod
    def verify_transaction(transaction, get_balance):
        ''' Verify a transaction the sender has sufficient coins '''
        sender_balance_account = get_balance(transaction.t_from)
        return sender_balance_account >= transaction.amount and Wallet.verify_transaction(transaction)

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = str([tx.tx_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        print(guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_blockchain(cls, blockchain):
        ''' returns 
            (true) if blockchain is valid : block has the same previous block hash
            (false) if blockchain is not valid = block != from previous block hash
        '''
        for (index, block) in enumerate(blockchain.chain):
            if index == 0:
                continue
            if block.previous_hash != Hash_util.hash_block(blockchain.chain[index - 1]):
                print(f'Invalid Hash at {block.previous_hash}')
                return False 
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Invalid proof of work')
                return False
        return True