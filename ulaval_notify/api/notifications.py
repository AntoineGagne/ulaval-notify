import sys

from requests import Request

from .constants import BASE_URL, NOTIFICATION_CALLBACKS_BY_PLATFORM_NAME
from ..utils import before


class NotificationManager:
    notification_route = '{base_url}/communication/v1/messagesimportants'.format(
        base_url=BASE_URL
    )

    def __init__(self, session_manager, callback):
        self._session_manager = session_manager
        self._callback = callback
        self._seen_notifications = set()
        self._request = self.__create_request()

    def __create_request(self):
        return Request(
            'GET',
            NotificationManager.notification_route,
            params={
                'idutilisateurmpo': self._session_manager.user_details.user_id,
                'statutpublication': 'PUBLIE'
            },
            headers={
                'Authorization': '{token_type} {token}'.format(
                    token_type=self._session_manager.token_details.token_type,
                    token=self._session_manager.token_details.token
                ),
                'Accept': 'application/json, text/plain, */*'
            }
        )

    def check_notifications(self):
        response = self._session_manager.send(self._request)
        if not response:
            return

        response = response.json()
        self._display_notifications(
            notification for notification in response.get('messagesImportants', ())
            if notification.get('idMessageImportant') not in self._seen_notifications
        )

    def _display_notifications(self, notifications):
        for notification in notifications:
            self._seen_notifications.add(notification.get('idMessageImportant'))
            self._callback(notification)


def send_linux_notification(notification):
    import notify2
    notify2.init('ulaval-notify')
    notification = notify2.Notification(
        'New notification',
        '{message}'.format(message=notification.get('messageHtml')),
        ''
    )
    notification.show()


def find_appropriate_notification_callback():
    for platform, callback in NOTIFICATION_CALLBACKS_BY_PLATFORM_NAME:
        if sys.platform.startswith(key):
            return callback

    return send_linux_notification
