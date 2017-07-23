#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import build
import process


def parse_args():

    parser = argparse.ArgumentParser(description='Run RTB functional client')
    parser.add_argument('-k', '--kernel', type=str,
                        help='Name of kernel to run.',
                        default='os161', dest='kernel')
    return parser.parse_args()


def main():

    args = parse_args()

    #for line in build.build_kernel_image_shell(args.kernel):
    #	print line
    
    build_name = build.build_kernel_image_shell(args.kernel)
    output = build.run_kernel(args.kernel, build_name)
    process.process_os161_tt1(output)


if __name__ == "__main__":
    main()
