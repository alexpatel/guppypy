#!/usr/bin/env python

import contextlib
import argparse
import os
import importlib
import shutil
import time

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
log = lambda p: "\n\033[;1m>>> " + p + "\033[0;0m"


def parse_args():
    parser = argparse.ArgumentParser(description='guppypy synthesis lib')
    parser.add_argument('-f', '--file', type=str,
			help='synthesis template to use',
			default='entry.S.jinja2', dest='synth_template')
    parser.add_argument('-s', '--synth', type=str,
			help='synthesizer to run (module.method)',
			default='stack_order.synthesize', dest='synth')
    parser.add_argument('-d', '--dest', type=str,
			help='path in barrelfish to put synthesized code',
			default='kernel/arch/x86_64/entry.S', dest='dest_path')
    return parser.parse_args()


@contextlib.contextmanager
def in_barrelfish_repo():
    """
    Context manager to run a set of commands within barrelfish repo.

    with in_barrelfish_repo():
        foo()
    """
    os.chdir('guppy')
    yield
    os.chdir('..')
 

def patch_commit(parent, synth_cand, dest_path, version):
    """Render a synthesis candidate into barrelfish tree and commit. """
    # assume cwd = guppy

    # render synthesized code as a Jinja2 child template that inherits the
    # source code it is being insert into as a parent
    inject_template = lambda cand: """
{{% extends "{}" %}}\n{{% block synthesize %}}\n{}{{% endblock %}}\n
    """.format(parent, cand)
    synth_child = inject_template(synth_cand)

    # write out child template to build/
    build_templ  = os.path.join('build',
                                '%s.jinja2' % version)
    with open(os.path.join('templates', build_templ), 'w') as f:
        f.write(synth_child)
    
    # render into target source
    synthesized = env.get_template(build_templ).render()
    synth_outf = '%s-rendered' % build_templ
    with open(os.path.join('templates', synth_outf), 'w') as f:
        f.write(synthesized)

    with in_barrelfish_repo():

        # checkout a new branch
        msg = 'Patching BarrelfishOS with synthesis candidate %s'
        print log(msg % version)
        os.system('git checkout -b %s' % version)

    # copy to barrelfish
    shutil.copyfile(os.path.join('templates', synth_outf),
                    os.path.join('guppy', dest_path))

    with in_barrelfish_repo():

        # commit to repo
        os.system('git add %s' % dest_path)
        os.system('git commit -m "[auto] add %s"' % version)
        #os.system('git push origin %s' % version)
    
    print log('Done patching BarrelfishOS source')


def build_barrelfish(version):
    """Build and run BarrelfishOS with Docker. """
    # assume cwd = guppy and git branch = version

    # build image
    print log('Building BarrelfishOS synthesis candidate  %s' % version)
    os.system('docker build . -t %s' % version)

    # run container
    print log('Testing BarrelfishOS synthesis candidate  %s' % version)
    os.system('docker run %s' % version)

    msg = 'If you got without kill -9, you probably passed :) (%s)'
    print log(msg % version)


def restore_barrelfish_trunk(version):
    os.system('git checkout dev')
   

def main():
    """
    Synthesize a program and then try it on BarrelfishOS.
    """

    # load arguments from CLI
    args = parse_args()

    # tag synthesizer version
    version = '%s_%s' % (args.synth.lower(), int(time.time()))
    print log('Starting synthesizer test version=%s' % version)

    msg = 'Loading synthesizer %s for template %s'
    print log(msg % (args.synth, args.synth_template))

    # load synthesize() function from -s flag
    mod, func = args.synth.rsplit('.', 1)
    mod = importlib.import_module(mod)
    synth_func = getattr(mod, func)

    # synthesize code
    print log('Running SMT to synthesize ASM to load stack registers')
    synth_candidates = synth_func()

    # render each synthesis candidate and add to guppy version control
    for ndx, cand in enumerate(synth_candidates):
	cand_ver = '%s_%s' % (version, str(ndx))

        # add candidate to version control
        patch_commit(args.synth_template, cand, args.dest_path, cand_ver)
        restore_barrelfish_trunk(cand_ver)

if __name__ == '__main__':
    main()
