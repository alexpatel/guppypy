#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from build import build_docker_image


def parse_args():

    parser = argparse.ArgumentParser(description='Run RTB functional client')
    parser.add_argument('-k', '--kernel', type=str,
                        help='Name of kernel to run.',
                        default='os161', dest='kernel')
    return parser.parse_args()

def main():

    args = parse_args()
    print args.kernel
    build_docker_image(args.kernel)


if __name__ == "__main__":
    main()
