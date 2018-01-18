"""This module contains the code related to the parsing of the command line options.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

import os.path
from argparse import ArgumentParser, FileType

from .utils import dummy_wrap, run_as_daemon


def parse_arguments():
    """Create an :class:`argparse.ArgumentParser` and parse the command-line
       arguments.
    """
    parser = ArgumentParser(prog='ulaval-notify',
                            description='Display when there is new '
                                        'notifications on monPortail')
    parser.add_argument('-d',
                        '--daemon',
                        action="store_const",
                        default=dummy_wrap,
                        const=run_as_daemon,
                        dest='daemonize',
                        help='run the program in the background (requires the '
                             '`python-daemon` package)')
    parser.add_argument('-t',
                        '--time-interval',
                        type=int,
                        required=False,
                        dest='time_interval',
                        default=60,
                        help='the interval at which the API is polled for '
                             'new notifications')
    parser.add_argument('-c',
                        '--configuration-file',
                        type=FileType('r'),
                        required=False,
                        dest='configuration_file',
                        default=open(os.path.expanduser('~/.ulaval-notify.ini')),
                        help='the configuration file that contains the '
                             'options such as the username and password '
                             '(default: ~/.ulaval-notify)')
    return parser.parse_args()
