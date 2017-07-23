# -*- coding: utf-8 -*-

"""
Insert a kprintf into the OS/161 thread creation routine and then check that it
worked with an experiment.
"""

import unittest

from guppypy.os_config import *
from guppypy.test_case import OS161ThreadTests
from guppypy.parser import ANSICFunction, ASCIC

# load OS/161 source
os161 = OSConfig('os161')

# create two identical images 
default_os = OSSynthesizer(os161, tag='default')
synth_os = OSSynthesizer(os161, tag='synth')

# modify thread_create() in the second image
func = ANSICFunction(synth_os, 'kern/thread/thread.c', 'thread_create')
with func.open():
    kprintf = ANSIC('kprintf("Creating new thread");')
    func.inject_beginning(kprintf)

# run TT1 against all containers, 3 times each
suite = unittst.TestSuite()
for i in range(3):
    for kernel in (synth_os, default_os):
        suite.add(OS161ThreadTests(kernel))

unittest.TextTestRunner().run(suite)

