import notify2

from requests import Request

from .constants import BASE_URL


NOTIFICATION_ROUTE = '{base_url}/communication/v1/messagesimportants'.format(
    base_url=BASE_URL
)

def check_notifications(session_manager, callback):
    request = Request(
        'GET',
        NOTIFICATION_ROUTE,
        params={
            'idutilisateurmpo': session_manager.user_details.user_id,
            'statutpublication': 'PUBLIE',
            'statutlecture': 'NON_VUE'
        },
        headers={
            'Authorization': '{token_type} {token}'.format(
                token_type=session_manager.token_details.token_type,
                token=session_manager.token_details.token
            ),
            'Accept': 'application/json, text/plain, */*'
        }
    )
    response = session_manager.send(request)
    callback(response.json() if response else {})



def send_linux_notification(notifications_details):
    messages_number = notifications_details.get('nombreTotalMessagesImportants')
    notify2.init('ulaval-notify')
    notification = notify2.Notification(
        'New notifications',
        '{messages_number}'.format(messages_number=messages_number),
        ''
    )
    notification.show()
