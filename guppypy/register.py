from pysmt.shortcuts import Symbol, Int, And, GE, LE, LT
from pysmt.typing import INT


class X86StackRegister(object):
    """
    A X86StackRegister is a logical atom. It stores a mapping a from x86_64
    register name to an slot index in the arguments user-space stack loaded into the
    kernel stack in a system call handler.
    """

    stack = range(0, 12)

    register_names = [
        '%r10', '%r11', '%r12', '%r13', '%r14', '%r15', '%r8', '%r9', '%rax', '%rbp',
        '%rbx', '%rcx'
    ]

    def __init__(self, name):
        assert name in X86StackRegister.register_names
        self.name = name
        self.sym = Symbol(name, INT)

    # condition: is a register that needs to be loaded from user-space stack
    def has_valid_stack_slot(self):
	return And(GE(self.sym, Int(min(self.stack))),
		   LE(self.sym, Int(max(self.stack)))) 

    # condition: needs to be loaded from user-space stack before register
    def precedes(self, register):
        return LT(self.sym, register.sym)

    def pushq(self):
        return '    pushq  %s' % (self.name)

    @classmethod
    def get_stack_registers(cls):
        return {name: cls(name) for name in cls.register_names}

    def get_stack_index(self, model):
        return model.get_py_value(self.sym)
