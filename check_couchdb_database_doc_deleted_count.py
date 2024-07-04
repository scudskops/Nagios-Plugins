#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2017-10-29 16:16:55 +0100 (Sun, 29 Oct 2017)
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

Nagios Plugin to check a CouchDB database's doc deleted count via its API

Outputs perfdata for graphing and optional thresholds are applied

Tested on CouchDB 1.6.1 and 2.1.0

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
    from check_couchdb_database_stats import CheckCouchDBDatabaseStats
except ImportError:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


class CheckCouchDBDatabaseDocDeletedCount(CheckCouchDBDatabaseStats):

    def __init__(self):
        # Python 2.x
        super(CheckCouchDBDatabaseDocDeletedCount, self).__init__()
        # Python 3.x
        # super().__init__()
        self.has_thresholds = True

    def check_couchdb_stats(self, json_data):
        doc_del_count = json_data['doc_del_count']
        self.msg += "doc deleted count = {0}".format(doc_del_count)
        self.check_thresholds(doc_del_count)
        self.msg += ' | doc_deleted_count={0}{1}'.format(doc_del_count, self.get_perf_thresholds())


if __name__ == '__main__':
    CheckCouchDBDatabaseDocDeletedCount().main()
