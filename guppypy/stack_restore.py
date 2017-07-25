#!/usr/env/bin python

"""
Use model checking to synthesize X86 assembly to restore user stack after
system call in BarrelfishOS.
"""

from pysmt.typing import INT
from pysmt.shortcuts import Symbol, Int, And, GE, LE, GT, get_model

from register import Register as REG


registers = dict(map(lambda r: (r, Symbol(r, INT)), [
    '%r10', '%r11', '%r12', '%r13', '%r14', '%r15', '%r8', '%r9', '%rax', '%rbp',
    '%rbx', '%rcx'
]))

stack = range(2, 14)
low, high = min(stack), max(stack)

def is_valid_stack_arg(reg):
    return And(LE(reg, Int(max(stack))), GE(reg, Int(min(stack)))) 

domain = [
    And(is_valid_stack_arg(reg) for reg in registers.values()),
    GT(registers['%rcx'], registers['%r11']), 
    GT(registers['%r11'], registers['%rbx']),
    GT(registers['%rbx'], registers['%rbp']),
    GT(registers['%rbp'], registers['%rax']),
    GT(registers['%rax'], registers['%r15']),
    GT(registers['%rax'], registers['%r15']),
    GT(registers['%r15'], registers['%r14']),
    GT(registers['%r14'], registers['%r13']),
    GT(registers['%r13'], registers['%r12']),
    GT(registers['%r12'], registers['%r9']),
    GT(registers['%r9'], registers['%r8']),
    GT(registers['%r8'], registers['%r10']),
]

problem = And(domain) 
model = get_model(problem)
if model:
    print model
else:
    print 'No solutions found.'
