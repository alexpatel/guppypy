from pysmt.shortcuts import Symbol, Int, And, GE, LE, LT, get_model
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


def synthesize():
    doc = """
    Synthesize the assembly for copying user-space stack arguments
    into the kernel.
    """     

    # dictionary of CPU registers, index by name
    regs = X86StackRegister.get_stack_registers()

    # x86_64 machine description
    stack_order_desc = And(
        # every register has to be brought onto the stack
        And(reg.has_valid_stack_slot() for reg in regs.values()),

        # x86 syscall callframe register order
        regs['%rcx'].precedes(regs['%r11']), 
        regs['%r11'].precedes(regs['%rbx']),
        regs['%rbx'].precedes(regs['%rbp']),
        regs['%rbp'].precedes(regs['%rax']),
        regs['%rax'].precedes(regs['%r15']),
        regs['%rax'].precedes(regs['%r15']),
        regs['%r15'].precedes(regs['%r14']),
        regs['%r14'].precedes(regs['%r13']),
        regs['%r13'].precedes(regs['%r12']),
        regs['%r12'].precedes(regs['%r9']),
        regs['%r9'].precedes(regs['%r8']),
        regs['%r8'].precedes(regs['%r10']),
    )
    
    # Use a SMT solver to figure out the order to pull register from user-space
    # onto the kernel stack

    model = get_model(stack_order_desc)
    stack = sorted(regs.values(), key=lambda r: r.get_stack_index(model))
    
    print '\nSYNTHESIZED CODE>>>\n'

    for reg in stack:
        print reg.pushq()
    
    # generate code
    asm = '\n'.join([reg.pushq() for reg in stack])

    return asm
