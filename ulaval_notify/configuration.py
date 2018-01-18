import configparser
from collections import namedtuple


ConfigurationOptions = namedtuple('ConfigurationOptions', ['authentication', 'general'])


class ConfigurationException(Exception):
    pass


def read_configuration_file(configuration_file):
    try:
        configuration_parser = configparser.ConfigParser(default_section='general')
        configuration_parser.read_file(configuration_file)
        return ConfigurationOptions(**configuration_parser)
    except TypeError:
        raise ConfigurationException(
            "Could not parse the configuration file. Perhaps there is a "
            "missing field or a typo?"
        )
