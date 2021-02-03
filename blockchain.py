from functools import reduce
import hashlib
import json
from collections import OrderedDict

#reward
BLOCK_MINING_REWARD = 10

# root Block :: first block
root_block  = {        
    'previous_hash': '1234',
    'index':0,
    'transactions': [],
    'proof':50
    }

# blockchain list
blockchain = [root_block]

# transactions list
transactions = []

# who
owner = 'Khalil'

# Nodes
participants = {owner}

def get_last_blockchain_value():
    ''' returns the last value of the blockchain '''
    if len(blockchain) < 1: 
        return [1] # init blockchain with 1 if it s empty
    return blockchain[-1]

def get_balance(participant): 
    ''' returns the balance of a participant'''  
    transactions_sent = [[transaction['amount'] for transaction in block['transactions']
                         if transaction['from'] == participant] for block in blockchain]
    
    # get amount from recent(sent) transactions [] which is not already added in the blockchain
    current_transaction = [transaction['amount']
                         for transaction in transactions if transaction['from'] == participant]
    
    transactions_sent.append(current_transaction) 
    # amount_sent sum with reduce function 
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                         if len(tx_amt) > 0 else tx_sum + 0, transactions_sent, 0)
    print(f'amount_sent {amount_sent}')
    transactions_received = [[transaction['amount'] for transaction in block['transactions'] if transaction['to'] == participant] for block in blockchain]
    
    # amount_reveived sum with reduce function 
    amount_reveived = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                     if len(tx_amt) > 0 else tx_sum + 0, transactions_received, 0)
    print(f'amount_reveived {amount_reveived}')
    return amount_reveived - amount_sent

def add_transaction( to_recipient, amount,from_sender=owner,):
    ''' appends a (new transaction amount) and the (last blockchain value) to blockchain '''
    # transaction = {
    #     'from':from_sender,
    #     'to':to_recipient,
    #      'amount':amount} 
    transaction = OrderedDict(
        [('from', from_sender), ('to', to_recipient), ('amount', amount)]) 
    if verify_transaction(transaction):
        transactions.append(transaction)
        return True
    return False

def hash_block(block):
    ''' returns hash of block based on values of his elements '''
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

  

def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(transactions))


def valid_proof(transactions, last_hash, proof):
    guess = str(transactions) + str(last_hash) + str(proof)
    guess_hash = hashlib.sha256(guess.encode()).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_block_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(transactions, last_block_hash,proof):
        proof += 1
    return proof



def verify_transaction(transaction):
    ''' Verify a transaction the sender has sufficient coins '''
    sender_balance_account = get_balance(transaction['from'])
    return sender_balance_account >= transaction['amount']

def mine_block():
    ''' simulate block mining on blockchain '''
    last_block = blockchain[-1]

    # hashed_block = hash_block(last_block)
    proof = proof_of_work()
    #reward transaction for miner
    # reward_transaction = {
    #     'from':'MINING_SYSTEM',
    #     'to':owner,
    #     'amount':BLOCK_REWARD
    # }
    reward_transaction = OrderedDict(
        [('from', 'MINING'), ('to', owner), ('amount', BLOCK_MINING_REWARD)])
    # get copy of transaction
    cp_transactions = transactions[:] 
    cp_transactions.append(reward_transaction)
    # add the new block
    block = {
        'previous_hash': hash_block(last_block),
        'index':len(blockchain),
        'transactions': cp_transactions, 
        'proof':proof
        }
    blockchain.append(block)
    save_data()
    return True


def get_user_input():
    ''' returns the user input as float '''
    # transaction_sender = input('Enter the sender of the transaction : ')
    transaction_recipient = input('Enter the recipent of the transaction : ')
    transaction_amount = float(input('Your transaction amout : '))
    return transaction_recipient,transaction_amount

def get_user_choice():
    ''' returns the user choice (string) '''
    return input('your choice : ')

def print_participants():
    ''' print participants '''
    print(participants)

def print_blockchain_blocks():
    ''' print blockchain '''
    for block in blockchain:
        print(block)

def verify_blockchain():
    ''' returns 
        (true) if blockchain is valid : block has the same previous block hash
        (false) if blockchain is not valid = block != from previous block hash
    '''
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            print('Invalid Hash')
            return False 
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Invalid proof of work')
            return False
    return True




while True:
    print(' -- Enter your choice -- ')
    print('[1] : add a new transaction amount')
    print('[2] : mine new block')
    print('[3] : output the blockchain')
    print('[4] : output participants')
    print('[q] : quit')
    # get user input
    user_choice = get_user_choice()
    # choice : 1
    if user_choice == '1':
        transaction_data = get_user_input()
        recipient,amount = transaction_data
        if add_transaction(to_recipient=recipient,amount=amount):
            print('Transaction succeeded !')
        else:
            print(f'Transaction failed ! : not enough money to transfer : you have only {amount}')
        print(transactions)
     # choice : 2
    elif user_choice == '2':
       if mine_block():
           transactions = []
           save_data()
    # choice : 3
    elif user_choice == '3':
        print_blockchain_blocks()
        # choice : 3
    elif user_choice == '4':
        print_participants()
    # quit 
    elif user_choice == 'q':
        break
    else:
        print('invalid input --> '+user_choice)
    if not verify_blockchain():
        print('invalid blockchain')
        break
    print(f'Account balance of {owner} is {get_balance(owner)}')

    
print('Finish !')
   