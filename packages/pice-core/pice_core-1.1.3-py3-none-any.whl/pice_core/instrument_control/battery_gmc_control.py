"""
This file is used to connect battery(SYSKON_P1500) via serial port.

@Author: Siwei.Lu
@Date: 2022.11.27
"""
import sys
import time

from . import serial_control


class BatGMCControlBySerial:
    def __init__(self, baud, com, vbat_config=None):
        self.__vbat_default_config = vbat_config
        self.__baud = baud
        self.__com = com

        try:
            self.__serialHandler = serial_control.SerialHandler(self.__com, self.__baud)
        except BaseException as err:
            print("power_supply_gmc({}) open failed! \n{}".format(self.__com, err))
            serial_control.logger.error("power_supply_gmc({}) open failed! \n{}".format(self.__com, err))
            sys.exit()

    def set_input_voltage(self, input_vol: float):
        vol_cmd = "USET {}\n".format(str(input_vol))
        self.__serialHandler.send_req(vol_cmd)

    def set_input_current(self, input_cur: float):
        cur_cmd = "ISET {}\n".format(str(input_cur))
        self.__serialHandler.send_req(cur_cmd)

    def set_output(self, output: str):
        cur_cmd = "output {}\n".format(output)
        self.__serialHandler.send_req(cur_cmd)

    def read_output_voltage(self):
        req_cmd = "UOUT?\n"
        self.__serialHandler.send_req(req_cmd)
        data = self.__serialHandler.rec_data()

        while True:
            if len(data) == 14:  # 判断接收数据长度是否为指定长度
                break
            else:
                self.__serialHandler.send_req(req_cmd)
                data = self.__serialHandler.rec_data()

        return float(str(data[6:].decode()))

    def read_output_current(self):
        req_cmd = "IOUT?\n"
        self.__serialHandler.send_req(req_cmd)
        data = self.__serialHandler.rec_data()

        while True:
            if len(data) == 14:  # 判断接收数据长度是否为指定长度
                break
            else:
                self.__serialHandler.send_req(req_cmd)
                data = self.__serialHandler.rec_data()

        return float(str(data[6:].decode()))

    def set_default_status(self):
        voltage = self.__vbat_default_config['default_input_voltage']
        current = self.__vbat_default_config['default_input_current']
        status = self.__vbat_default_config['default_status']

        self.set_input_current(current)
        self.set_input_voltage(voltage)
        self.set_output(status)

    def power_reset(self):
        self.set_output('off')
        time.sleep(1)
        self.set_output('on')
