"""
This file defines the global variables only used for test report.

@Author: Yanjiao.Li
@Date: 2022.12.13
@Update: 2023.02.13
"""

import socket
import time

g_computer_ip = socket.gethostbyname(socket.gethostname())
g_department = "Test"
g_time = time.strftime("%Y/%m/%d  %H:%M:%S  %A", time.localtime(time.time()))
g_tester = None
g_report_title = None
g_project = None
g_sample = None
g_variant = None
g_bootloader = None
g_HW = None
g_SW = None
g_tag = None
g_dataset = None
g_expected = None
g_actually = None
g_testScriptID = None
g_testcaseID = None
g_url = None


def information(tester, report_title, project, sample, variant, bootloader, HW, SW, tag, dataset):
    global g_tester
    global g_report_title
    global g_project
    global g_sample
    global g_variant
    global g_bootloader
    global g_HW
    global g_SW
    global g_tag
    global g_dataset

    g_tester = tester
    g_report_title = report_title
    g_project = project
    g_sample = sample
    g_variant = variant
    g_bootloader = bootloader
    g_HW = HW
    g_SW = SW
    g_tag = tag
    g_dataset = dataset
