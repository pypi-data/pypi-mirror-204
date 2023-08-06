"""
This file is used to connect battery(KORAD) via serial port.

@Author: Bo.Li
@Date: 2022.12.09
"""
import sys
import time

from . import serial_control


class BatKoradControlBySerial:
    def __init__(self, baud, com, vbat_config=None):
        self.__vbat_default_config = vbat_config
        self.__baud = baud
        self.__com = com

        try:
            self.__serialHandler = serial_control.SerialHandler(self.__com, self.__baud)
        except BaseException as err:
            print("power_supply_korad({}) open failed! \n{}".format(self.__com, err))
            serial_control.logger.error("power_supply_korad({}) open failed! \n{}".format(self.__com, err))
            sys.exit()

    def set_input_voltage(self, input_vol: float):
        vol_cmd = "VSET1:{}\n".format(str(input_vol))
        self.__serialHandler.send_req(vol_cmd)

    def set_input_current(self, input_cur: float):
        cur_cmd = "ISET1:{}\n".format(str(input_cur))
        self.__serialHandler.send_req(cur_cmd)

    def set_output(self, output: str):
        if output == "on":
            req = 1
        else:
            req = 0
        cur_cmd = "OUT{}\n".format(req)
        self.__serialHandler.send_req(cur_cmd)

    def read_output_voltage(self):
        req_cmd = "VOUT1?:"
        self.__serialHandler.send_req(req_cmd)
        data = self.__serialHandler.rec_data()

        # print(float(str(data.decode())))
        return float(str(data.decode()))

    def read_output_current(self):
        req_cmd = "IOUT1?:"
        self.__serialHandler.send_req(req_cmd)
        data = self.__serialHandler.rec_data()

        # print(float(str(data.decode())))
        return float(str(data.decode()))

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
