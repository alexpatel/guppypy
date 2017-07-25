#!/usr/env/bin python

"""
Use model checking to synthesize X86 assembly to restore user stack after
system call in BarrelfishOS.
"""

from jinja2 import Template
from pysmt.typing import INT
from pysmt.shortcuts import Symbol, Int, And, GE, LE, LT, get_model

from register import Register as REG

def create_symbols(registers):
    return {
        reg: Symbol(reg, INT) for reg in registers
    }

registers = create_symbols([
    '%r10', '%r11', '%r12', '%r13', '%r14', '%r15', '%r8', '%r9', '%rax', '%rbp',
    '%rbx', '%rcx'
])

stack = range(2, 14)
first_index, last_index= min(stack), max(stack)

def is_valid_stack_arg(reg):
    return And(GE(reg, Int(first_index)), LE(reg, Int(last_index))) 

domain = [
    And(is_valid_stack_arg(reg) for reg in registers.values()),
    LT(registers['%rcx'], registers['%r11']), 
    LT(registers['%r11'], registers['%rbx']),
    LT(registers['%rbx'], registers['%rbp']),
    LT(registers['%rbp'], registers['%rax']),
    LT(registers['%rax'], registers['%r15']),
    LT(registers['%rax'], registers['%r15']),
    LT(registers['%r15'], registers['%r14']),
    LT(registers['%r14'], registers['%r13']),
    LT(registers['%r13'], registers['%r12']),
    LT(registers['%r12'], registers['%r9']),
    LT(registers['%r9'], registers['%r8']),
    LT(registers['%r8'], registers['%r10']),
]

problem = And(domain) 
model = get_model(problem)
if model:
    print model
else:
    print 'No solutions found.'


def custom_function(a):
    return a.replace('o', 'ay')

template = 'Hey, my name is {{ custom_function(first_name) }}'
jinga_html_template = Template(template)
jinga_html_template.globals['custom_function'] = custom_function

fields = {'first_name': 'Jo'}
#print jinga_html_template.render(**fields)

def synthesize():
    return 'false'

t = Template(open('entry.S.synth', 'r').read())
print t.render(synthesize=synthesize)
