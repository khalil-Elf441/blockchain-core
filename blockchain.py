from functools import reduce
import hashlib
import json
# import pickle
from collections import OrderedDict
from block import Block
from transaction import Transaction
from Utility.verification_util import Verification_util
from Utility.hash_util import Hash_util
from wallet import Wallet

#reward
BLOCK_MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        # root Block :: first block
        root_block  = Block(0,'',[],50)
        #initializing blockchain list
        self.__chain = [root_block]
        # transactions list
        self.__transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @property
    def transactions(self):
        return self.__transactions[:]
    

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                # print(file_content)
                blockchain = json.loads(file_content[0][:-1])
                #load blockchain
                load_blockchain = []
                for block in blockchain:
                    conv_transaction = [Transaction(tx['t_from'],tx['t_to'],tx['signature'],tx['amount']) for tx in block['transactions']]
                    formated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        conv_transaction,
                        block['proof'],
                        block['timestamp']
                    )
                    load_blockchain.append(formated_block)
                self.__chain = load_blockchain
                #load transactions
                op_transactions  = json.loads(file_content[1])
                load_transactions = []
                for tx in op_transactions:
                    formated_transaction = Transaction(
                        tx['t_from'],
                        tx['t_to'],
                        tx['signature'],
                        tx['amount'])
                    # formated_transaction = OrderedDict(
                    #     [('from', tx['from']), ('to', tx['to']), ('amount', tx['amount'])])
                    load_transactions.append(formated_transaction)
                self.__transactions  = load_transactions
        except (IndexError,IOError) as e:
            print(e)
        finally:
            print("loading finish !")    

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                sv_chain = [block.__dict__ for block in [
                    Block(
                        block_item.index,
                        block_item.previous_hash,
                        [tx.__dict__ for tx in block_item.transactions],
                        block_item.proof,
                        block_item.timestamp) for block_item in self.__chain]]

                f.write(json.dumps(sv_chain))
                f.write('\n')

                sv_transactions = [tx.__dict__ for tx in self.transactions]
                f.write(json.dumps(sv_transactions))
        except IOError:
            print('saving failed !')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_block_hash = Hash_util.hash_block(last_block)
        proof = 0
        while not Verification_util.valid_proof(self.transactions, last_block_hash,proof):
            proof += 1
        return proof  


    def get_last_blockchain_value(self):
        ''' returns the last value of the blockchain '''
        if len(self.__chain) < 1: 
            return None
        return self.__chain[-1]

    def get_balance(self, participant): 
        ''' returns the balance of a participant'''  
        transactions_sent = [[transaction.amount for transaction in block.transactions
                            if transaction.t_from == participant] for block in self.__chain]
        
        # get amount from recent(sent) transactions [] which is not already added in the blockchain
        current_transaction = [transaction.amount
                            for transaction in self.transactions if transaction.t_from == participant]
        
        transactions_sent.append(current_transaction) 
        # amount_sent sum with reduce function 
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                            if len(tx_amt) > 0 else tx_sum + 0, transactions_sent, 0)
        print(f'amount_sent {amount_sent}')
        transactions_received = [[transaction.amount for transaction in block.transactions
         if transaction.t_to == participant] for block in self.__chain]
        
        # amount_reveived sum with reduce function 
        amount_reveived = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                        if len(tx_amt) > 0 else tx_sum + 0, transactions_received, 0)
        print(f'amount_reveived {amount_reveived}')
        return amount_reveived - amount_sent

    def add_transaction(self, to_recipient, from_sender, signature, amount):
        ''' appends a (new transaction amount) and the (last blockchain value) to blockchain '''
        
        if self.hosting_node == None:
            return False
        
        transaction = Transaction(
            from_sender,
            to_recipient,
            signature,
            amount
        )   
        if not Wallet.verify_transaction(transaction):
            print("Transation dont match Public Key !")
            return False
        if Verification_util.verify_transaction(transaction, self.get_balance):
            self.__transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        ''' simulate block mining on blockchain '''

        
        if self.hosting_node == None:
            return False

        last_block = self.__chain[-1]

        # hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        reward_transaction = Transaction('MINING', self.hosting_node,'', BLOCK_MINING_REWARD)

        # get copy of transaction
        cp_transactions = self.transactions[:] 
        if not cp_transactions:
            for tx in cp_transactions:
                if not Wallet.verify_transaction(tx):
                    return False
        cp_transactions.append(reward_transaction)
        # add the new block
        block = Block(
            len(self.__chain),
            Hash_util.hash_block(last_block),
            cp_transactions, 
            proof
        )

        self.__chain.append(block)
        self.__transactions = []
        self.save_data()      
        return True    