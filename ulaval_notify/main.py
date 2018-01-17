import getpass

from time import sleep

import requests

from .api.login import User, login
from .api.notifications import NotificationManager, send_linux_notification
from .api.session import refresh_periodically
from .constants import SESSION_REFRESH_INTERVAL_IN_SECONDS
from .options import parse_arguments


def main():
    arguments = parse_arguments()
    _main(arguments)


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
            send_linux_notification
        )
        refresh_periodically(SESSION_REFRESH_INTERVAL_IN_SECONDS, session_manager)

        while True:
            notification_manager.check_notifications()
            sleep(arguments.refresh_interval)
            continue
