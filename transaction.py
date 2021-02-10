from collections import OrderedDict


class Transaction:
    def __init__(self, t_from, t_to, signature, amount):
        self.t_from = t_from
        self.t_to = t_to
        self.amount = amount
        self.signature = signature
    
    def tx_ordered_dict(self):
        return OrderedDict([('t_from', self.t_from), ('t_to',self.t_to), ('amount', self.amount)])

    def __repr__(self) -> str:
        return str(self.__dict__)
