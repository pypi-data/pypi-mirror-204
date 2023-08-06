"""
This file is used to connect battery(NGI) via serial port.

@Author: Chengyu.Liu Yujie.Shi
@Date: 2022.12.6
"""
import sys
import time

from . import serial_control


class BatControlNGIBySerial:
    def __init__(self, baud, com, vbat_config=None):
        self.__vbat_default_config = vbat_config
        self.__baud = baud
        self.__com = com

        try:
            self.__serialHandler = serial_control.SerialHandler(self.__com, self.__baud)
        except BaseException as err:
            print("power_supply_ngi({}) open failed! \n{}".format(self.__com, err))
            serial_control.logger.error("power_supply_ngi({}) open failed! \n{}".format(self.__com, err))
            sys.exit()

    def send(self, data):
        # 通过串口下发字符串，通常用于对下位机下发字符串指令
        self.__serialHandler.send_req(data)

    def set_input_voltage(self, input_vol: float):
        vol_cmd = 'SOURce:VOLTage ' + str(input_vol) + ' \n'
        self.send(vol_cmd)

    def set_input_current(self, input_cur: float):
        vol_cmd = 'SOURce:CURRent ' + str(input_cur) + ' \n'
        self.send(vol_cmd)

    def set_output(self, status: str):
        output_cmd = 'OUTPut:ONOFF ' + str(status) + ' \n'
        self.send(output_cmd)

    def read_output_voltage(self):
        cmd = 'MEASure:VOLTage? \n'
        self.send(cmd)
        data = self.__serialHandler.rec_data()

        while True:
            if len(data) == 8:  # 判断接收数据长度是否为指定长度
                break
            else:
                self.send(cmd)
                data = self.__serialHandler.rec_data()

        return data.decode()

    def read_output_current(self):
        cmd = 'MEASure:CURRent? \n'
        self.send(cmd)
        data = self.__serialHandler.rec_data()

        while True:
            if len(data) == 9:  # 判断接收数据长度是否为指定长度
                break
            else:
                self.send(cmd)
                data = self.__serialHandler.rec_data()

        return data.decode()

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
