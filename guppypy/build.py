#!/usr/bin/env python

import os
import io

import docker

_client = None


def get_os_path(kernel):
    """Get absolute path of kernel in os/. """
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'os', kernel)
    return path


def get_client(api_client=False):
    """Get Docker API client. """

    global _client
    if not _client: 
        if api_client:
            _client = docker.APIClient(base_url='unix://var/run/docker.sock')
        else:
            _client = docker.from_env()
    return _client


def get_dockerfile_fileobj(os_path):
    """Load a dockerfile for an OS kernel. """

    dockerfile_path = os.path.join(os_path, 'Dockerfile')
    print os_path
    print dockerfile_path
    with open(dockerfile_path, 'r') as dockerfile:
        contents = dockerfile.read()
        return io.BytesIO(contents.encode('utf-8'))


def build_docker_image(kernel):
    """Build docker image for an OS kernel. """

    os_path = get_os_path(kernel)
    dockerfile_fileobj = get_dockerfile_fileobj(os_path)
    tag = 'guppypy/{}'.format(kernel)

    # build image
    docker_client = get_client(api_client=True)
    stream = docker_client.build(fileobj=dockerfile_fileobj, tag=tag)
    for ndx, line in enumerate(stream):
        print str(ndx) + ': ' + line
