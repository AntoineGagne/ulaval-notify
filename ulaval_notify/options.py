from argparse import ArgumentParser

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
                        dest='refresh_interval',
                        default=60,
                        help='the interval at which the API is polled for '
                             'new notifications')
    return parser.parse_args()
