#!/usr/bin/env python


def process_os161_tt1(output):

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
