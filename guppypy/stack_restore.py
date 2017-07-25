# This is the tutorial example of pySMT.
#
# This example shows how to:
# 1. Deal with Theory atoms
# 2. Specify a solver in the shortcuts (get_model, is_sat etc.)
# 3. Obtain an print a model
#
#
# The goal of the puzzle is to assign a value from 1 to 10 to each letter s.t.
#    H+E+L+L+O = W+O+R+L+D = 25
#
from pysmt.shortcuts import Symbol, And, GE, LT, Plus, Equals, Int, get_model
from pysmt.typing import INT

registers = {
    'RIP': 	'%rcx',		# user-space RIP
    'RFLAGS': 	'%r11',		# user-space RFLAGS
    'RSP': 	'%rsp',		# user-space stack pointer
    11: 	'%rbx',		# arg11
    10: 	'%rbp',		# arg10
    9: 		'%rax',		# arg9
    8: 		'%r15',		# arg8
    7: 		'%r14',		# arg7
    6: 		'%r13',		# arg6
    5: 		'%r12',		# arg5 
    4: 		'%r9',		# arg4
    3: 		'%r8',		# arg3
    2: 		'%r10',		# arg2
    '5f_src': 	'%r11',		# source register of 5th function arg
    '5f_dest': 	'%r8',		# dest register of 5th function arg	
    '6f_src': 	'%rcx',		# source register of 6th function arg
    '6f_dest': 	'%r9',		# dest register of 6th function arg	
    '4f_src': 	'%rsp',		# source register of 4th function arg
    '4f_dest': 	'%rcx',		# dest register of 4th function arg	
}

hello = [Symbol(s, INT) for s in 'hello']
world = [Symbol(s, INT) for s in 'world']
letters = set(hello+world)
domains = And([And(GE(l, Int(1)),
                   LT(l, Int(10))) for l in letters])

sum_hello = Plus(hello) # n-ary operators can take lists
sum_world = Plus(world) # as arguments
problem = And(Equals(sum_hello, sum_world),
              Equals(sum_hello, Int(25)))
formula = And(domains, problem)

print('Serialization of the formula:')
print(formula)

model = get_model(formula)
if model:
    print(model)
else:
    print('No solution found')
