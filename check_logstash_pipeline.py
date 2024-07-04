#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2017-11-24 21:10:35 +0100 (Fri, 24 Nov 2017)
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

Nagios Plugin to check a Logstash pipeline is online via the Logstash Rest API

API is only available in Logstash 5.x onwards, will get connection refused on older versions

Optional thresholds apply to the number of pipeline workers

Ensure Logstash options:
  --http.host should be set to 0.0.0.0 if querying remotely
  --http.port should be set to the same port that you are querying via this plugin's --port switch

Tested on Logstash 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.0, 6.1

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
    #from harisekhon.utils import log
    from harisekhon.utils import ERRORS, UnknownError, support_msg_api
    from harisekhon.utils import validate_chars
    from harisekhon import RestNagiosPlugin
except ImportError:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.6'


class CheckLogstashPipeline(RestNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckLogstashPipeline, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = 'Logstash'
        self.default_port = 9600
        # could add pipeline name to end of this endpoint but error would be less good 404 Not Found
        # Logstash 5.x /_node/pipeline <= use -5 switch for older Logstash
        # Logstash 6.x /_node/pipelines
        self.path = '/_node/pipelines'
        self.auth = False
        self.json = True
        self.msg = 'Logstash pipeline msg not defined yet'
        self.pipeline = None

    def add_options(self):
        super(CheckLogstashPipeline, self).add_options()
        self.add_opt('-i', '--pipeline', default='main', help='Pipeline to expect is configured (default: main)')
        self.add_opt('-d', '--dead-letter-queue-enabled', action='store_true',
                     help='Check dead letter queue is enabled on pipeline (optional, only applies to Logstash 6+)')
        self.add_opt('-5', '--logstash-5', action='store_true',
                     help='Logstash 5.x (has a slightly different API endpoint to 6.x)')
        self.add_opt('-l', '--list', action='store_true', help='List pipelines and exit (only for Logstash 6+)')
        self.add_thresholds()

    def process_options(self):
        super(CheckLogstashPipeline, self).process_options()
        self.pipeline = self.get_opt('pipeline')
        validate_chars(self.pipeline, 'pipeline', 'A-Za-z0-9_-')
        # slightly more efficient to not return the potential list of other pipelines but the error is less informative
        #self.path += '/{}'.format(self.pipeline)
        if self.get_opt('logstash_5'):
            if self.pipeline != 'main':
                self.usage("--pipeline can only be 'main' for --logstash-5")
            if self.get_opt('list'):
                self.usage('can only --list pipelines for Logstash 6+')
            if self.get_opt('dead_letter_queue_enabled'):
                self.usage('--dead-letter-queue-enabled only available with Logstash 6+')
            self.path = self.path.rstrip('s')
        self.validate_thresholds(simple='lower', optional=True)

    def parse_json(self, json_data):
        if self.get_opt('logstash_5'):
            pipeline = json_data['pipeline']
        else:
            pipelines = json_data['pipelines']
            if self.get_opt('list'):
                print('Logstash Pipelines:\n')
                for pipeline in pipelines:
                    print(pipeline)
                sys.exit(ERRORS['UNKNOWN'])
            pipeline = None
            if self.pipeline in pipelines:
                pipeline = pipelines[self.pipeline]
        self.msg = "Logstash pipeline '{}' ".format(self.pipeline)
        if pipeline:
            self.msg += 'exists'
            if 'workers' not in pipeline:
                raise UnknownError('workers field not found, Logstash may still be initializing' + \
                                   '. If problem persists {}'.format(support_msg_api()))
            workers = pipeline['workers']
            self.msg += ' with {} workers'.format(workers)
            self.check_thresholds(workers)
            if not self.get_opt('logstash_5'):
                dead_letter_queue_enabled = pipeline['dead_letter_queue_enabled']
                self.msg += ', dead letter queue enabled: {}'.format(dead_letter_queue_enabled)
                if self.get_opt('dead_letter_queue_enabled') and not dead_letter_queue_enabled:
                    self.warning()
                    self.msg += ' (expected True)'
            batch_delay = pipeline['batch_delay']
            batch_size = pipeline['batch_size']
            self.msg += ', batch delay: {}, batch size: {}'.format(batch_delay, batch_size)
        else:
            self.critical()
            self.msg += 'does not exist!'


if __name__ == '__main__':
    CheckLogstashPipeline().main()
