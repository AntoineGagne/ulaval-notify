import getpass

from time import sleep

import requests

from .api.login import User, login
from .api.notifications import (NotificationManager,
                                find_appropriate_notification_callback,
                                create_request)
from .api.session import refresh_periodically
from .constants import SESSION_REFRESH_INTERVAL_IN_SECONDS
from .options import parse_arguments


def main():
    arguments = parse_arguments()
    arguments.daemonize(_main, arguments)


def _main(arguments):
    with requests.Session() as session:
        username = input('Username: ')
        password = getpass.getpass()
        session_manager = login(
            session,
            User(username=username, password=password)
        )
        notification_manager = NotificationManager(
            session_manager,
            find_appropriate_notification_callback(),
            create_request
        )
        refresh_periodically(SESSION_REFRESH_INTERVAL_IN_SECONDS, session_manager)

        while True:
            notification_manager.check_notifications()
            sleep(arguments.time_interval)
            continue
