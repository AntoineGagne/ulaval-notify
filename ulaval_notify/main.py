import getpass

from time import sleep

import requests

from .api.login import User, login
from .api.notifications import check_notifications, send_linux_notification
from .api.session import refresh_periodically
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
        refresh_periodically(arguments.refresh_interval, session_manager)
        while True:
            check_notifications(session_manager, send_linux_notification)
            sleep(60)
            continue
