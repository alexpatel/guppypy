# -*- coding: utf-8 -*-

import unittest

from os_config import OSBuilder


class OS161ThreadTests(unittest.TestCase, OSBuilder):

    def check_pass(output):
        """Check that TT1 passed. """

	prompt = 'OS/161 kernel [? for menu]: '
	test_init, test_conclude = prompt + 'tt1', prompt + 'q'

	test_result = []
	found = False
	
	for line in output:

	    if test_init in line:
		found = True
		continue

	    if test_conclude in line:
		assert found
		break

	    if found:
		test_result.append(line)

	for line in test_result:
	    print line

	self.assertTrue(found)

    def test_tt1(self):
        """Run TT1 thread test. """

	os_path = get_os_path(self.name)
	cmd = 'cd {} && docker run {}'.format(self.os_path, self.build_name)
	return os.popen(cmd).readlines()
	return self.check_pass(output)
