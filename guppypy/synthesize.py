#!/usr/env/bin python

import argparse
import os
import importlib
import time

from jinja2 import Template

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

    # chdir into barrelfish source repository
    os.chdir('guppy')

    # checkout a new branch
    os.system('git checkout -b %s' % version)

    # put file in repo
    with open(dest_path, 'w') as dest_file:
	dest_file.write(file_contents)

    # commit
    os.system('git add %s' % dest_path)
    os.system('git commit -m "[auto] add %s"' % version)

    # build a docker image with the synthesized code
    os.system('docker build . -t %s' % version)
    os.system('docker run %s' % version)

    # restore to trunk
    os.system('git checkout dev')

    # go back to pythonland
    os.chdir('..')


def main():
    # load arguments from CLI
    args = parse_args()

    # name synthesizer version ('entry_S_synth_10298149812')
    templ_esc = args.synth_template.replace('.', '_').lower()
    synth_version = '%s_%s' % (templ_esc, int(time.time()))

    # load synthesize() function from -s flag
    mod, func = args.synth.rsplit('.', 1)
    mod = importlib.import_module(mod)
    synth_func = getattr(mod, func)
    
    # load Jinja2 template in templates/ from -f flag
    template = os.path.join('templates', args.synth_template)
    t = Template(open(template, 'r').read())

    # synthesize code
    synth_output = t.render(synthesize=synth_func)

    # commit synthesized code to barrelfish and test it on QEMU/x86
    commit_and_test(synth_output, args.dest_path, synth_version)

,
if __name__ == '__main__':
    main()
