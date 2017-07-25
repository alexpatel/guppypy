#!/usr/env/bin python

"""
Use model checking to synthesize X86 assembly to restore user stack after
system call in BarrelfishOS.
"""

from jinja2 import Template
from pysmt.typing import INT
from pysmt.shortcuts import Symbol, Int, And, GE, LE, GT, get_model

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



def custom_function(a):
    return a.replace('o', 'ay')

template = 'Hey, my name is {{ custom_function(first_name) }}'
jinga_html_template = Template(template)
jinga_html_template.globals['custom_function'] = custom_function

fields = {'first_name': 'Jo'}
print jinga_html_template.render(**fields)
