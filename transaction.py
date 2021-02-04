from collections import OrderedDict


class Transaction:
    def __init__(self, t_from, t_to, amount):
        self.t_from = t_from
        self.t_to = t_to
        self.amount = amount
    
    def tx_ordered_dict(self):
        return OrderedDict([('from', self.t_from), ('to',self.t_to), ('amount', self.amount)])
