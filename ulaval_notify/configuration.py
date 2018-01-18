import configparser
from collections import namedtuple


ConfigurationOptions = namedtuple('ConfigurationOptions', ['authentication', 'general'])


def read_configuration_file(configuration_file):
    configuration_parser = configparser.ConfigParser(default_section='general')
    configuration_parser.read_file(configuration_file)
    return ConfigurationOptions(**configuration_parser)
