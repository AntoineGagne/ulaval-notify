"""This module contains the code related to the application execution.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

import sys
from time import sleep

import requests

from .api.login import User, login
from .api.notifications import (NotificationManager,
                                find_appropriate_notification_callback,
                                create_request)
from .api.session import refresh_periodically
from .constants import SESSION_REFRESH_INTERVAL_IN_SECONDS
from .configuration import read_configuration_file
from .options import parse_arguments


def main():
    """The main entry point of the application."""
    arguments = parse_arguments()
    arguments.daemonize(_main, arguments)


def _main(arguments):
    with requests.Session() as session:
        configuration_options = read_configuration_file(
            arguments.configuration_file
        )
        session_manager = login(
            session,
            User(**configuration_options.authentication)
        )
        notification_manager = NotificationManager(
            session_manager,
            find_appropriate_notification_callback(sys.platform),
            create_request
        )
        refresh_periodically(SESSION_REFRESH_INTERVAL_IN_SECONDS, session_manager)

        while True:
            notification_manager.check_notifications()
            sleep(arguments.time_interval)
            continue
