"""
This file is used to connect read_current/voltage_module(KV_AMP) via serial port.

Refer to KV_AMPxxx系列微电流表头-用户手册V1.0.pdf and KV_DVMxxx系列电压表头-用户手册V1.1.pdf
for the relevant calculation formulae.

@Author: Siwei.Lu
@Date: 2022.11.27
"""
import sys

import time

from ..parse_config_file import parse_config
from . import serial_control


class ReadCurrVolModuleControl:
    def __init__(self, baud, com):
        self.__baud = baud
        self.__com = com
        self.__read_req = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02]

        try:
            self.__serialHandler = serial_control.SerialHandler(self.__com, self.__baud)
        except BaseException as err:
            print("read_current_voltage_module({}) open failed! \n{}".format(self.__com, err))
            serial_control.logger.error("read_current_voltage_module({}) open failed! \n{}".format(self.__com, err))
            sys.exit()

    def read_current(self, addr):
        Resolution = 0.1
        cur_cmd = self.__read_req.copy()
        cur_cmd[0] = addr

        current = self._send_and_rec(cur_cmd)

        if (current[3] == 0xFF) and (current[4] == 0xFF):
            return -round((0xFFFF - current[5] * 0x100 - current[6]) * Resolution * Resolution, 3)  # mA

        return round((current[5] * 0x100 + current[6]), 3) * Resolution  # mA

    def read_voltage(self, addr):
        Resolution = 1  # 1mV
        vol_cmd = self.__read_req.copy()
        vol_cmd[0] = addr

        voltage = self._send_and_rec(vol_cmd)

        if (voltage[3] == 0xFF) and (voltage[4] == 0xFF):
            return -round((0xFFFF - voltage[5] * 0x100 - voltage[6]) * Resolution * Resolution * 0.001, 3)  # mV 转 V

        return round((voltage[5] * 0x100 + voltage[6]), 3) * Resolution * 0.001  # mV 转 V

    def _send_and_rec(self, request_cmd: list):
        for i in range(2):  # 发2次命令，避免接收数据不对
            cmd = request_cmd.copy()
            self.__serialHandler.send_req(self.__serialHandler.get_array_after_crc16(cmd))
            data = self.__serialHandler.rec_data()
            time.sleep(0.5)

        while True:
            if len(data) == 9:  # 判断接收数据长度是否为指定长度
                break
            else:
                cmd = request_cmd.copy()
                self.__serialHandler.send_req(self.__serialHandler.get_array_after_crc16(cmd))
                data = self.__serialHandler.rec_data()

        return data
