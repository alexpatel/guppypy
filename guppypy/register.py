from pysmt.shortcuts import Symbol, Int, Equals, TRUE, And
from pysmt.typing import INT


class Register(object):

    def __init__(self, reg_name):
        self.name = reg_name
	self.ident = 'reg_%s' % (reg_name)
	self.slot = Symbol(self.ident, INT)

    def __str__(self):
        return self.name

    def stack_order_constraint(self, reg):
	if self.slot_index >= reg.slot_index:
	    return GE(self.slot, reg2.slot)
	return TRUE()

    def assign_slot(self, slot_index):
	self.slot_index = slot_index
	return Equals(self.slot, Int(self.slot_index))

    def has_valid_slot(self):
	return And(GE(self.slot, Int(min(slots))), LE(self.slot, Int(max(slots))))
