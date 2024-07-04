#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2020-03-27 22:34:24 +0000 (Fri, 27 Mar 2020)
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

Nagios Plugin to check the health of a GoCD server via its API

Tested on GoCD 20.2.0

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import traceback
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon import RestNagiosPlugin
except ImportError:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


# pylint: disable=too-few-public-methods
class CheckGoCDServerHealth(RestNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckGoCDServerHealth, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = 'GoCD'
        self.default_port = 8153
        self.path = '/go/api/v1/health'
        self.auth = 'optional'
        self.json = True
        self.msg = 'GoCD msg not defined yet'

    def parse_json(self, json_data):
        health = json_data['health']
        if health != 'OK':
            self.critical()
        self.msg = 'GoCD server health = {}'.format(health)


if __name__ == '__main__':
    CheckGoCDServerHealth().main()
