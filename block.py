from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, transactions, proof, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time
    
    def __repr__(self) -> str:
        return str(self.__dict__)
