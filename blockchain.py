
# blockchain list
blockchain = []


def get_last_blockchain_value():
    ''' returns the last value of the blockchain '''
    if len(blockchain) < 1: 
        return [1] # init blockchain with 1 if it s empty
    return blockchain[-1]

def add_transaction(amount, last_transaction=get_last_blockchain_value()):
    ''' appends a (new transaction amount) and the (last blockchain value) to blockchain '''
    blockchain.append([last_transaction, amount])

def get_user_input():
    ''' returns the user input as float '''
    return float(input('Your transaction amout : '))

def get_user_choice():
    ''' returns the user choice (string) '''
    return input('your choice : ')

def print_blockchain_blocks():
    for block in blockchain:
        print(block)

def verify_blockchain():
    ''' returns 
        (true) if blockchain is valid : block has the same previous block hash
        (false) if blockchain is not valid = block != from previous block hash
    '''
    index = 1
    for block in blockchain:
        if block[0] != blockchain[index - 1]:
            return False
        else:
            index += 1
    
    return True


while True:
    print(' -- Enter your choice -- ')
    print('[1] : add a new transaction amout')
    print('[2] : output the blockchain')
    print('[q] : quit')
    # get user input
    user_choice = get_user_choice()
    # choice : 1
    if user_choice == '1':
        transaction_amout = get_user_input()
        add_transaction(transaction_amout)
    # choice : 2
    elif user_choice == '2':
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
   