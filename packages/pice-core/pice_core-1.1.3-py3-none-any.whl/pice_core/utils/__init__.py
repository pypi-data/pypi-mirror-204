import os

from ..can_related import parse_canoe_tools
from ..veristand_related import gen_mapping
from ..cb_related.codebeamer_connect import CodeBeamerHandler

work_path = os.path.abspath('.')


def gen_cdd_name_def():
    try:
        print("work_path = ", work_path)
        cdd = parse_canoe_tools.CddHandler(work_path)
        cdd.write_cdd_qualifier_to_enum_class(work_path)
    except BaseException as err:
        print(err)


def gen_dbc_name_def():
    try:
        print("work_path = ", work_path)
        dbc = parse_canoe_tools.CANoeToolHandler(work_path)
        dbc.write_msg_sig_to_enum_class(work_path)
    except BaseException as err:
        print(err)


def gen_ni_map_def():
    try:
        print("work_path = ", work_path)
        gen_mapping.gen_mapping_function(work_path)
    except BaseException as err:
        print(err)


def gen_pdx_name_def():
    try:
        print("work_path = ", work_path)
        pdx = parse_canoe_tools.PDXHandler(work_path)
        pdx.write_pdx_data_to_enum_class(work_path)
    except BaseException as err:
        print(err)


def gen_sys_name_def():
    try:
        print("work_path = ", work_path)
        sysvar = parse_canoe_tools.SysHandler(work_path)
        sysvar.write_sys_namespace_variable_to_enum_class(work_path)
    except BaseException as err:
        print(err)


def gen_testcase_from_cb():
    try:
        print("work_path = ", work_path)
        print("Enter codebeamer Account name:")
        name = input()
        print("Enter codebeamer Password:")
        password = input()

        print("\nStart create test case file...")

        cb = CodeBeamerHandler(work_path, name, password)
        cb.write_case_to_py()

        print("\ntest case write successfully! \n")

    except BaseException as err:
        print(err)
