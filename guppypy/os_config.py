# -*- coding: utf-8 -*-

import io
import os
import shutil
import tarfile
import time

import docker

_client = None
_os_paths = {}


class BaseOSMixin(object):

    def __init__(self, os_config):
        self.os_config = os_config
        self.name = self.os_config.name


class OSBuilder(BaseOSMixin):

    def __init__(self, *args, **kwargs):
        super(OSBuilder, self).__init__(*args, **kargs)
        self.now = int(time.time())
        self.build_name = '{}-{}'.format(self.config.name, int(time.time()))
        self.os_path = self.get_os_path()

    def get_os_path(self):
        """Get absolute path of kernel in os/. """

        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'os', self.name)
        return path

    def copyin_dockerfile(self):
        """Copy dockerfile into kernel repository. """

        dockerfile_path = os.path.join(self.os_path, 'Dockerfile')
        dockerfile_cp_path = os.path.join(self.os_path, 'src', 'Dockerfile')
        shutil.copyfile(dockerfile_path, dockerfile_cp_path)

    def build_kernel_image_shell(self):
        """Build docker image for an OS kernel using shell command. """

        src_path = os.path.join(self.os_path, 'src')
        self.copyin_dockerfile()
        cmd = 'cd {} && docker build . -t {}'
        os.system(cmd.format(self.os_path, self.build_name))


class OSSynthesizer(BaseOSMixin):

    def __init__(self, tag='default') 
        super(OSSynthesizer, self).__init__(*args, **kargs)
        self.tag = tag


class OSConfig(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
