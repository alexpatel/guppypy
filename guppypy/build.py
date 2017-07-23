#!/usr/bin/env python

import io
import os
import shutil
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
 

def get_docker_client(api_client=False):
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


def copyin_dockerfile(kernel_name):
    """Copy dockerfile into kernel repository. """

    os_path = get_os_path(kernel_name)
    dockerfile_path = os.path.join(os_path, 'Dockerfile')
    dockerfile_cp_path = os.path.join(os_path, 'src', 'Dockerfile')
    shutil.copyfile(dockerfile_path, dockerfile_cp_path)


def build_kernel_image(kernel_name):
    """Build docker image for an OS kernel using Docker SDK. """

    build_name = get_build_name(kernel_name)
    os_path = get_os_path(kernel_name)

    build_tag = 'guppypy/{}'.format(build_name)
    build_context = create_tarball(kernel_name, build_name)

    # build image
    docker_client = get_docker_client(api_client=True)
    build = docker_client.build(fileobj=build_context, tag=build_tag,
                                custom_context=True, encoding="gzip")
    for line in build:
        print line


def build_kernel_image_shell(kernel_name):
    """Build docker image for an OS kernel using shell command. """

    os_path = get_os_path(kernel_name)
    src_path = os.path.join(os_path, 'src')
    copyin_dockerfile(kernel_name)
    build_name = get_build_name(kernel_name)
    cmd = 'cd {} && docker build . -t {}'.format(os_path, build_name)
    os.system(cmd)
    return build_name


def run_kernel(kernel_name, build_name):
    """Run a test aginast a kernel. """

    os_path = get_os_path(kernel_name)
    cmd = 'cd {} && docker run {}'.format(os_path, build_name)
    return os.popen(cmd).readlines()
