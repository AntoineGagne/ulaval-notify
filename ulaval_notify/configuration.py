"""This module contains the code related to the configuration file.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""
import configparser
from collections import namedtuple


#: The available sections in the configuration file
ConfigurationOptions = namedtuple('ConfigurationOptions', ['authentication', 'general'])


class ConfigurationException(Exception):
    """An exception that occurs when there was an error in the configuration
       file.
    """
    pass


def read_configuration_file(configuration_file):
    """Read the given configuration file.

    :param configuration_file: The configuration file to parse
    :returns: The parsed configuration options
    :raises ConfigurationException: Raised when there was an error in the
                                    configuration file
    """
    try:
        configuration_parser = configparser.ConfigParser(default_section='general')
        configuration_parser.read_file(configuration_file)
        return ConfigurationOptions(**configuration_parser)
    except TypeError:
        raise ConfigurationException(
            "Could not parse the configuration file. Perhaps there is a "
            "missing field or a typo?"
        )
