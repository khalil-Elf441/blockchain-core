
from blockchain import Blockchain
from uuid import uuid4
from Utility.verification_util import Verification_util


class Node:
    def __init__(self) -> None:
        self.node_id = str(uuid4())
        self.blockchain = Blockchain(self.node_id)


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
            print('[1] : add a new transaction amount')
            print('[2] : mine new block')
            print('[3] : output the blockchain')
            print('[4] : output participants')
            print('[q] : quit')
            # get user input
            user_choice = self.get_user_choice()
            # choice : 1
            if user_choice == '1':
                transaction_data = self.get_user_input()
                recipient,amount = transaction_data
                if self.blockchain.add_transaction(to_recipient=recipient,from_sender=self.node_id,amount=amount):
                    print('Transaction succeeded !')
                else:
                    print(f'Transaction failed ! : not enough money to transfer : you have only {amount}')
                print(self.blockchain.transactions)
            # choice : 2
            elif user_choice == '2':
                 self.blockchain.mine_block()                
            # choice : 3
            elif user_choice == '3':
                self.print_blockchain_blocks()
                # choice : 3
            # elif user_choice == '4':
            #     print_participants()
            # quit 
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
                print('invalid blockchain')
                break
            print(f'Account balance of {self.node_id} is {self.blockchain.get_balance(self.node_id)}')


node = Node()
node.listen_for_requests()