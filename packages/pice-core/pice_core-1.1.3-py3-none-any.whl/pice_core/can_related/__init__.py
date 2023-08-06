from ..parse_config_file import parse_config
from .can_control import Msg
from ..instrument_control import default_config


def connect_can_control_by_vector_hardware(config: parse_config.ConfigHandler = default_config, can_fd=True):
    serial = config.get_config_by_name('vector_hardware')['serial_number']
    channel = config.get_config_by_name('vector_hardware')['channel']

    return Msg(serial, channel, can_fd)
