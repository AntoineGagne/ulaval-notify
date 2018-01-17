from argparse import ArgumentParser


def parse_arguments():
    """Create an :class:`argparse.ArgumentParser` and parse the command-line
       arguments.
    """
    parser = ArgumentParser(prog='ulaval-notify',
                            description='Display when there is new '
                                        'notifications on monPortail')
    parser.add_argument('-d',
                        '--daemon',
                        action="store_true",
                        default=False,
                        dest='is_daemon',
                        help='run the program in the background')
    parser.add_argument('-t',
                        '--time-interval',
                        type=int,
                        required=False,
                        dest='refresh_interval',
                        default=60,
                        help='the interval at which the session is refreshed')
    return parser.parse_args()
