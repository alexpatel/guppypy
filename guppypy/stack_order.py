"""
Synthesize the x86_64 BarrelfishOS ASM for loading the user-space syscall
arguments onto the kernel stack during a CPU driver system call handler.
"""

import random

from pysmt.shortcuts import get_model

from x86_64 import machine_description, X86StackRegister

# dictionary of CPU registers, indexed by name
regs = X86StackRegister.get_stack_registers()

# x86_64 syscall user call conventions spec
machine_desc = machine_description(regs)


def SMTSynthesizer():
    """
    Use SMT to solve the ordering of register loads based on call conventions
    """     

    print '> SMT synthesizer'
    
    # Use a SMT solver to figure out the order to pull register values from
    # user-space stack onto the kernel stack
    model = get_model(machine_desc)
    stack = sorted(regs.values(), key=lambda r: r.get_stack_index(model))
    return X86StackRegister.pushqs(stack)


def RandomSynthesizer():
    """
    Pull the registers values off of the user stack in random order.
    """

    print '> Random synthesizer'

    stack = X86StackRegister.get_stack_registers().values()
    random.shuffle(stack)
    return X86StackRegister.pushqs(stack)


def synthesize():
    return {
        'smt': SMTSynthesizer(),
        'rand-1': RandomSynthesizer(),
        'rand-2': RandomSynthesizer(),
    }
