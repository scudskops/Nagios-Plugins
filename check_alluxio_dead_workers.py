#!/usr/bin/env python3
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2016-02-02 17:46:18 +0000 (Tue, 02 Feb 2016)
#
#  https://github.com/HariSekhon/Nagios-Plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback
#  to help improve or steer this or other code I publish
#
#  https://www.linkedin.com/in/HariSekhon
#

"""

Nagios Plugin to check the number of dead Alluxio workers via the Alluxio Master UI

Tested on Alluxio 1.0.0, 1.0.1, 1.1.0

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import os
import sys
import traceback
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pylib'))
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from check_tachyon_dead_workers import CheckTachyonDeadWorkers
except ImportError:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.4.0'


class CheckAlluxioDeadWorkers(CheckTachyonDeadWorkers):

    def __init__(self):
        # Python 2.x
        super(CheckAlluxioDeadWorkers, self).__init__()
        # Python 3.x
        # super().__init__()
        self.software = 'Alluxio'
        self.name = ['Alluxio Master', 'Alluxio']


if __name__ == '__main__':
    CheckAlluxioDeadWorkers().main()
