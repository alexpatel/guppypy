#!/usr/env/bin python

from jinja2 import Template
from pysmt.shortcuts import And, get_model
from register import X86StackRegister


def synthesize():
    """
    Use an SMT solver to synthesize the assembly for copying user-space stack
    arguments into the kernel.
    """     

    # CPU registers
    regs = X86StackRegister.get_stack_registers()

    # machine description
    stack_ordering = And(
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
        
    # solve stack order
    model = get_model(stack_ordering)
    stack = sorted(regs.values(), key=lambda r: r.get_stack_index(model))

    print "\nSYNTHESIZED CODE>>>\n"
    for reg in stack:
        print reg.get_stack_index(model), reg.pushq()
    
    # generate code
    asm = '\n'.join([reg.pushq() for reg in stack])

    return asm


t = Template(open('entry.S.synth', 'r').read())
print t.render(synthesize=synthesize)
