"""This module contains the code related to the notifications handling.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

from requests import Request
from pkg_resources import resource_filename

from .constants import BASE_URL


def create_request(session_manager):
    """Create the request to fetch notifications.

    :param session_manager: The session manager that holds the details
                            necessary to do the request
    :returns: The newly built request
    """
    notification_route = '{base_url}/communication/v1/messagesimportants'.format(
        base_url=BASE_URL
    )
    return Request(
        'GET',
        notification_route,
        params={
            'idutilisateurmpo': session_manager.user_details.user_id,
            'statutpublication': 'PUBLIE'
        }
    )


class NotificationManager:
    """The notification manager checks for new notifications.

    :param session_manager: The API session manager
    :param callback: The callback that will send the notification to the OS
                     specific notification manager
    :param create_request: A callable that will be used to create the request
                           to the API
    """

    def __init__(self, session_manager, callback, create_request):
        """Construct a new notification manager."""
        self._session_manager = session_manager
        self._callback = callback
        self._seen_notifications = set()
        self._create_request = create_request

    def check_notifications(self):
        """Check for new notifications."""
        response = self._session_manager.send(self._create_request(self._session_manager))
        if not response:
            return

        self._display_notifications(
            notification for notification
            in response.get('messagesImportants', ())
            if notification.get('idMessageImportant')
            not in self._seen_notifications
        )

    def _display_notifications(self, notifications):
        for notification in notifications:
            self._seen_notifications.add(
                notification.get('idMessageImportant')
            )
            self._callback(notification)


def send_linux_notification(notification):
    """Send a notification with the `libnotify` library.

    :param notification: The notification to display
    """
    import notify2
    notify2.init('ulaval-notify')
    notification = notify2.Notification(
        'New notification',
        '{message}'.format(message=notification.get('messageHtml')),
        resource_filename('ulaval_notify', 'resources/images/ulaval-logo.png')
    )
    notification.show()


def find_appropriate_notification_callback(platform_name):
    """Find the appropriate notification sender given the platform name.
    
    :param platform_name: The name of the platform the application is running
                          on
    :returns: The appropriate callback to send notifications according to the
              platform name
    """
    notification_callbacks_by_platform_name = {
        'linux': send_linux_notification
    }

    notification_callback = send_linux_notification
    for platform, callback in notification_callbacks_by_platform_name.items():
        if platform_name.startswith(platform):
            notification_callback = callback

    return notification_callback
