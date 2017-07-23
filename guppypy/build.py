#!/usr/bin/env python

import io
import os
import tarfile
import time

import docker

_client = None
_os_paths = {}


def get_os_path(kernel):
    """Get absolute path of kernel in os/. """

    if kernel not in _os_paths:
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'os', kernel)
        _os_paths[kernel] = path
    return _os_paths[kernel]
 

def get_client(api_client=False):
    """Get Docker API client. """

    global _client
    if not _client: 
        if api_client:
            _client = docker.APIClient(base_url='unix://var/run/docker.sock')
        else:
            _client = docker.from_env()
    return _client


def get_tarball_dir():
    """Get path of place to put kernel context tarballs. """

    dir = os.path.dirname(__file__)
    return os.path.join(dir, 'tar')


def create_tarball(kernel_name, build_name):
    """Create kernel Docker build context tarball. """
    
    os_path = get_os_path(kernel_name)
    tarname = os.path.join(get_tarball_dir(), build_name)
    with tarfile.open(tarname, "w:gz") as tar:
        tar.add(os_path, arcname=os.path.basename(os_path))
    return tarname


def get_build_name(kernel_name):
    return '{}-{}'.format(kernel_name, int(time.time()))


def build_kernel_image(kernel_name):
    """Build docker image for an OS kernel. """

    build_name = get_build_name(kernel_name)
    os_path = get_os_path(kernel_name)

    build_tag = 'guppypy/{}'.format(build_name)
    build_context = create_tarball(kernel_name, build_name)

    # build image
    docker_client = get_client(api_client=True)
    stream = docker_client.build(fileobj=dockerfile_fileobj, tag=tag)
    for ndx, line in enumerate(stream):
        print str(ndx) + ': ' + line
