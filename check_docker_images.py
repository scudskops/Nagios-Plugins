#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2018-03-05 19:10:02 +0000 (Mon, 05 Mar 2018)
#
#  https://github.com/HariSekhon/Nagios-Plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/HariSekhon
#

"""

Nagios Plugin to check the number of Docker images via the Docker API

Optional thresholds can be applied and perfdata is output for graphing the number of images over time

Supports TLS with similar options to official 'docker' command

Tested on Docker 18.02

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import sys
import traceback
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import log, jsonpp
    from harisekhon import DockerNagiosPlugin
except ImportError:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


class CheckDockerImages(DockerNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckDockerImages, self).__init__()
        # Python 3.x
        # super().__init__()
        self.msg = 'Docker msg not defined yet'

    def add_options(self):
        super(CheckDockerImages, self).add_options()
        self.add_thresholds()

    def process_options(self):
        super(CheckDockerImages, self).process_options()
        self.validate_thresholds(integer=True, positive=True, optional=True)

    def check(self, client):
        log.info('running Docker info')
        info = client.info()
        if log.isEnabledFor(logging.DEBUG):
            log.debug(jsonpp(info))
        images = info['Images']
        self.msg = 'Docker images = {}'.format(images)
        self.check_thresholds(images)
        self.msg += ' | docker_images={}{}'.format(images, self.get_perf_thresholds())


if __name__ == '__main__':
    CheckDockerImages().main()
