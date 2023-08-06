"""
This file is used to connect battery(chroma) visa.

@Author: Yujie.shi
@Date: 2022.12.09
"""

import sys
import time

import pyvisa as visa

from . import serial_control


class BatChromaControlByVisa:
    def __init__(self, resource, vbat_config=None):
        self.__vbat_config = vbat_config
        self.__visa = resource
        rm = visa.ResourceManager("C:/Windows/System32/visa32.dll")

        try:
            self._inst = rm.open_resource(self.__visa)
        except BaseException as err:
            print("power_supply_chroma({}) open failed! \n{}".format(self.__visa, err))
            serial_control.logger.error("power_supply_chroma({}) open failed! \n{}".format(self.__visa, err))
            sys.exit()

    def set_output(self, status):
        self._inst.write("CONFigure:OUTPut {}\n".format(status))

    def set_input_voltage(self, input_vol: float):
        self._inst.write("SOUR:VOLT " + str(input_vol) + "\n")

    def set_input_current(self, input_cur: float):
        self._inst.write("SOUR:CURR " + str(input_cur) + "\n")

    def read_output_voltage(self):
        data = self._inst.query("FETC:VOLT?")
        return eval(data)

    def read_output_current(self):
        data = self._inst.query("FETCH:CURRent?")
        return eval(data)

    def power_reset(self):
        self._inst.write("CONFigure:OUTPut OFF\n")
        time.sleep(1)
        self._inst.write("CONFigure:OUTPut ON\n")

    def set_default_status(self):
        voltage = self.__vbat_config['default_input_voltage']
        current = self.__vbat_config['default_input_current']
        status = self.__vbat_config['default_status']

        self.set_input_current(current)
        self.set_input_voltage(voltage)
        self.set_output(status)


class BatChromaControlBySerial:
    def __init__(self, baud, com, vbat_config=None):
        self.__vbat_config = vbat_config
        self.__baud = baud
        self.__com = com

        try:
            self.__serialHandler = serial_control.SerialHandler(self.__com, self.__baud)
        except BaseException as err:
            print("power_supply_korad({}) open failed! \n{}".format(self.__com, err))
            serial_control.logger.error("power_supply_Chroma({}) open failed! \n{}".format(self.__com, err))
            sys.exit()

    def set_input_voltage(self, input_vol: float):
        vol_cmd = "SOUR:VOLT {}\n".format(str(input_vol))
        self.__serialHandler.send_req(vol_cmd)

    def set_input_current(self, input_cur: float):
        cur_cmd = "SOUR:CURR {}\n".format(str(input_cur))
        self.__serialHandler.send_req(cur_cmd)

    def send(self, cmd):
        self.__serialHandler.send_req(cmd)
        data = self.__serialHandler.rec_data()
        print(data)

        # print(float(str(data.decode())))
        return float(str(data.decode()))

    def set_output(self, output: str):
        cur_cmd = "CONFigure:OUTPut {}\n".format(output)
        self.__serialHandler.send_req(cur_cmd)

    def read_output_voltage(self):
        req_cmd = "FETC:VOLT?\n"
        self.__serialHandler.send_req(req_cmd)
        data = self.__serialHandler.rec_data()

        # print(float(str(data.decode())))
        return float(str(data.decode()))

    def set_default_status(self):
        voltage = self.__vbat_config['default_input_voltage']
        current = self.__vbat_config['default_input_current']
        status = self.__vbat_config['default_status']

        self.set_input_current(current)
        self.set_input_voltage(voltage)
        self.set_output(status)

