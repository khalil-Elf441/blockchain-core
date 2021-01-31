

# root Block :: first block
root_block  = {        
    'previous_hash': '1234',
    'index':0,
    'transactions': []
    }

# blockchain list
blockchain = [root_block]

# transactions list
transactions = []

# who
owner = 'Khalil'


def get_last_blockchain_value():
    ''' returns the last value of the blockchain '''
    if len(blockchain) < 1: 
        return [1] # init blockchain with 1 if it s empty
    return blockchain[-1]

def add_transaction( to_recipient, amount,from_sender=owner,):
    ''' appends a (new transaction amount) and the (last blockchain value) to blockchain '''
    transaction = {
        'from':from_sender,
        'to':to_recipient,
         'amount':amount}  
    transactions.append(transaction)

def hash_block(block):
    ''' returns hash of block based on values of his elements '''
    return '&'.join([str(block[key]) for key in block])

def mine_block():
    ''' simulate block mining on blockchain '''
    last_block = blockchain[-1]
    block = {
        'previous_hash': hash_block(last_block),
        'index':len(blockchain),
        'transactions': transactions
        }
    blockchain.append(block)

def get_user_input():
    ''' returns the user input as float '''
    # transaction_sender = input('Enter the sender of the transaction : ')
    transaction_recipient = input('Enter the recipent of the transaction : ')
    transaction_amount = float(input('Your transaction amout : '))
    return transaction_recipient,transaction_amount

def get_user_choice():
    ''' returns the user choice (string) '''
    return input('your choice : ')

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
            return False 
    return True


while True:
    print(' -- Enter your choice -- ')
    print('[1] : add a new transaction amout')
    print('[2] : mine new block')
    print('[3] : output the blockchain')
    print('[q] : quit')
    # get user input
    user_choice = get_user_choice()
    # choice : 1
    if user_choice == '1':
        transaction_data = get_user_input()
        recipient,amount = transaction_data
        add_transaction(to_recipient=recipient,amount=amount)
        print(transactions)
     # choice : 2
    elif user_choice == '2':
        mine_block()
    # choice : 3
    elif user_choice == '3':
        print_blockchain_blocks()
    # quit 
    elif user_choice == 'q':
        break
    else:
        print('invalid input --> '+user_choice)
    if not verify_blockchain():
        print('invalid blockchain')
        break
else:
    print('Finish !')
   