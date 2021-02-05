import hashlib
import json 

class Hash_util:
    def hash_block(block):
        ''' returns hash of block based on values of his elements '''
        hashable_block = block.__dict__.copy()
        hashable_block['transactions'] = [tx.tx_ordered_dict() for tx in hashable_block['transactions']]
        return hashlib.sha256(json.dumps(hashable_block, sort_keys=True).encode()).hexdigest()