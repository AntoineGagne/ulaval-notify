import pytest

from io import StringIO

from ulaval_notify.configuration import read_configuration_file, ConfigurationException


def test_that_given_a_bad_configuration_file_when_read_configuration_file_then_throws_ConfigurationException():
    invalid_configuration_file = StringIO(
        '[atuhentication]'
        '\nusername = test'
        '\npassword = test_password'
    )

    with pytest.raises(ConfigurationException):
        read_configuration_file(invalid_configuration_file)


def test_that_given_a_valid_configuration_file_when_read_configuration_file_then_returns_ConfigurationOptions():
    valid_configuration_file = StringIO(
        '[authentication]'
        '\nusername = test'
        '\npassword = test_password'
    )

    read_configuration_file(valid_configuration_file)
