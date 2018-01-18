from unittest import mock

import pytest

from ulaval_notify.api.notifications import NotificationManager
from ulaval_notify.api.session import SessionManager


AN_IMPORTANT_MESSAGE_ID = 1


@pytest.fixture
def session_manager_mock():
    session_manager = mock.create_autospec(SessionManager)
    session_manager.send.return_value = {
        'messagesImportants': [{
            'idMessageImportant': AN_IMPORTANT_MESSAGE_ID
        }]
    }
    return session_manager


@pytest.fixture
def callback_stub():
    return mock.MagicMock()


@pytest.fixture
def create_request_stub():
    return mock.MagicMock()


def test_that_given_already_displayed_notifications_when_check_notifications_then_no_notifications_are_displayed(session_manager_mock, callback_stub, create_request_stub):
    notification_manager = NotificationManager(
        session_manager_mock,
        callback_stub,
        create_request_stub
    )
    notification_manager.check_notifications()

    notification_manager.check_notifications()

    callback_stub.assert_called_once_with(mock.ANY)
