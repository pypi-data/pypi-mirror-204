"""
BatItechControlBySerial is used to connect battery(ITECH_IT6512) via serial port.
BatIT6512ControlByVisa is used to connect battery(ITECH_IT6512) via VISA.

@Author: Siwei.Lu & Chengyu.Liu
@Date: 2022.12.6
"""
import sys
import pyvisa
import time

from ..parse_config_file import parse_config
from . import serial_control


class BatItechControl:
    """
    目前不能使用串口控制
    """

    def __init__(self, config: parse_config.ConfigHandler):
        self.__config = config
        self.__vbat_config = self.__config.get_config_by_inst('power_supply_itech')
        self.__baud = self.__config.get_baud_rate('power_supply_itech')
        self.__com = self.__config.get_com('power_supply_itech')

        try:
            self.__serialHandler = serial_control.SerialHandler(self.__com, self.__baud)
        except BaseException as err:
            print("power_supply_itech({}) open failed! \n{}".format(self.__com, err))
            serial_control.logger.error("power_supply_itech({}) open failed! \n{}".format(self.__com, err))
            sys.exit()

    def set_input_voltage(self, input_vol: float):
        vol_cmd = "VOLT {}\n".format(str(input_vol))
        self.__serialHandler.send_req(vol_cmd)

    def set_input_current(self, input_cur: float):
        cur_cmd = "CURR {}\n".format(str(input_cur))
        self.__serialHandler.send_req(cur_cmd)

    def set_output(self, output: str):
        cur_cmd = "OUTPUT {}\n".format(output)
        self.__serialHandler.send_req(cur_cmd)

    def read_output_voltage(self):
        req_cmd = "VOLT?\n"
        self.__serialHandler.send_req(req_cmd)
        data = self.__serialHandler.rec_data()

        return data


class BatIT6512ControlByVisa:
    def __init__(self, resource, vbat_config=None):
        rm = pyvisa.ResourceManager()

        self.__vbat_config = vbat_config
        self.__resource = resource

        try:
            self.it6512 = rm.open_resource(self.__resource)
        except BaseException as err:
            print("power_supply_itech({}) open failed! \n{}".format(self.__resource, err))
            serial_control.logger.error("power_supply_itech({}) open failed! \n{}".format(self.__resource, err))
            sys.exit()

    def set_input_voltage(self, input_vol: float):
        vol_cmd = "VOLT {}\n".format(str(input_vol))
        self.it6512.write(vol_cmd)

    def set_input_current(self, input_cur: float):
        cur_cmd = "CURR {}\n".format(str(input_cur))
        self.it6512.write(cur_cmd)

    def set_output(self, output: str):
        output_cmd = "OUTP {}\n".format(output)
        self.it6512.write(output_cmd)

    def read_output_voltage(self):
        req_cmd = "MEASure:VOLT?\n"
        data = self.it6512.query(req_cmd)

        return data

    def read_output_current(self):
        req_cmd = "MEASure:CURR?\n"
        data = self.it6512.query(req_cmd)

        return data

    def set_default_status(self):
        voltage = self.__vbat_config['default_input_voltage']
        current = self.__vbat_config['default_input_current']
        status = self.__vbat_config['default_status']

        self.set_input_current(current)
        self.set_input_voltage(voltage)
        self.set_output(status)

    def power_reset(self):
        self.set_output('off')
        time.sleep(1)
        self.set_output('on')

    # def read_output_current():
    #   req_cmd = "CURR?\n"
