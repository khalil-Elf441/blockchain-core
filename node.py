
from blockchain import Blockchain
from uuid import uuid4
from Utility.verification_util import Verification_util
from wallet import Wallet


class Node:
    def __init__(self):
        # self.node_id = str(uuid4())
        # self.node_id = '32555250-b9df-41bd-aa18-2165e5101586'
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)


    def get_user_choice(self):
        ''' returns the user choice (string) '''
        return input('your choice : ')

    def get_user_input(self):
        ''' returns the user input as float '''
        # transaction_sender = input('Enter the sender of the transaction : ')
        transaction_recipient = input('Enter the recipent of the transaction : ')
        transaction_amount = float(input('Your transaction amount : '))
        return transaction_recipient,transaction_amount

    def print_blockchain_blocks(self):
        ''' print blockchain '''
        for block in self.blockchain.chain:
            print(block)

    def listen_for_requests(self):
        while True:
            print(' -- Enter your choice -- ')
            print('[1] : Add a new transaction amount')
            print('[2] : Mine new block')
            print('[3] : Output the blockchain')
            print('[4] : Create Wallet')
            print('[5] : Load Wallet')
            print('[6] : Save Wallet keys')
            print('[q] : Quit')
            # get user input
            user_choice = self.get_user_choice()
            # choice : 1
            if user_choice == '1':
                transaction_data = self.get_user_input()
                recipient,amount = transaction_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(to_recipient=recipient,from_sender=self.wallet.public_key, signature=signature,amount=amount):
                    print('Transaction succeeded !')
                else:
                    print(f'Transaction failed ! : not enough money to transfer : you have only {self.blockchain.get_balance(self.wallet.public_key)}')
                print(self.blockchain.transactions)
            # choice : 2
            elif user_choice == '2':
                 if not self.blockchain.mine_block():
                     print('Mining failed ! : No wallet')              
            # choice : 3
            elif user_choice == '3':
                self.print_blockchain_blocks()
            # choice : 4
            elif user_choice == '4':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            # choice : 5
            elif user_choice == '5':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            # choice : 6    
            elif user_choice == '6':
                self.wallet.save_keys()
            # choice : q
            elif user_choice == 'q':
                if self.blockchain.transactions:
                    print('Some transactions are not saved in block !')
                    final_choice = input('Do you want to continue anyway? [y/n] ')
                    if final_choice == 'y':
                        break
                else:
                    break
            else:
                print('invalid input --> '+user_choice)
            if not Verification_util.verify_blockchain(self.blockchain):
                print('Invalid blockchain : Verification goes wrong')
                break
            print(f'Account balance of {self.wallet.public_key[0:5]} is {self.blockchain.get_balance(self.wallet.public_key)}')

if __name__ == '__main__':
    node = Node()
    node.listen_for_requests()