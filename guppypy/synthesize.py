#!/usr/bin/env python

import argparse
import os
import importlib
import time

from jinja2 import Template

log = lambda p: "\n\033[;1m" + p + "\033[0;0m"


def parse_args():
    parser = argparse.ArgumentParser(description='guppypy synthesis lib')
    parser.add_argument('-f', '--file', type=str,
			help='synthesis template to use',
			default='entry.S.synth', dest='synth_template')
    parser.add_argument('-s', '--synth', type=str,
			help='synthesizer to run (module.method)',
			default='stack_order.synthesize', dest='synth')
    parser.add_argument('-d', '--dest', type=str,
			help='path in barrelfish to put synthesized code',
			default='kernel/arch/x86_64/entry.S', dest='dest_path')
    return parser.parse_args()


def commit_and_test(file_contents, dest_path, version):
    """
    Patch BarrelfishOS with synthesis candidate and test with Docker
    """

    # work with BarrelfishOS source
    print log('>>> Patching BarrelfishOS with synthesis candidate %s' % version)
    os.chdir('guppy')

    # checkout a new branch
    os.system('git checkout -b %s' % version)

    # put file in repo
    with open(dest_path, 'w') as dest_file:
	dest_file.write(file_contents)

    # commit to repo
    os.system('git add %s' % dest_path)
    os.system('git commit -m "[auto] add %s"' % version)

    # test with Docker
    print log('>>> Testing BarrelfishOS synthesis candidate  %s' % version)
    os.system('docker build . -t %s' % version)
    os.system('docker run %s' % version)

    # restore to trunk
    msg = '>>> If you got without kill -9, you probably passed :) (%s)'
    print log(msg % version)
    os.system('git checkout dev')

    # go back to pythonland
    os.chdir('..')


def main():
    """
    Synthesize a program and then try it on BarrelfishOS.
    """

    # load arguments from CLI
    args = parse_args()

    # name synthesizer version ('entry_S_synth_10298149812')
    version = '%s_%s' % (args.synth.lower(), int(time.time()))
    print log('Start synthesizer test version=%s' % version)

    msg = 'Loading synthesizer %s for template %s'
    print log(msg % (args.synth, args.synth_template))

    # load synthesize() function from -s flag
    mod, func = args.synth.rsplit('.', 1)
    mod = importlib.import_module(mod)
    synth_func = getattr(mod, func)
    
    # load Jinja2 template in templates/ from -f flag
    template = os.path.join('templates', args.synth_template)
    t = Template(open(template, 'r').read())

    # synthesize code
    print log('Start SMT solver to gen ASM to load user-space stack registers')
    synth_output = t.render(synthesize=synth_func)

    # commit synthesized code to barrelfish and test it on QEMU/x86
    print log('Test synthesis candidate %s against BarrelfishOS' % version)
    commit_and_test(synth_output, args.dest_path, version)


if __name__ == '__main__':
    main()
