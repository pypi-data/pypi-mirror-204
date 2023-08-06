'''
This file is used to turn mapping txt files into veristand channels

@Author: Zhihong.Lin
@Date: 2023.3.15
'''

# 从mapping文件导入veristand的通道变量

from ..parse_config_file import parse_config

base_yaml_path = '/test_fixture/test_configuration/config.yaml'


# read
def gen_mapping_function(project_name):
    project_config_path = project_name + base_yaml_path
    config = parse_config.ConfigHandler(project_config_path)
    file_path = config.get_config_by_name('NI_tools')['mapping_file_path']

    with open(file_path, "r") as f:
        para_list = []
        lines = f.readlines()
        data = ['from niveristand.clientapi import ChannelReference\r\n']
        for line in lines:
            # 根据条件修改
            if '=' not in line:  # 只修改一次，如果已经修改过则不需要修改
                last_file = line.split('/')[-1]
                sec_file = line.split('/')[-2]
                sec_file = sec_file.replace(" ", "").replace(".", "_").replace("-", "_").replace('(', '_').replace(')', '')
                temp = last_file.replace(" ", "").replace(".", "_").replace("-", "_").replace('(', '_').replace(')', '')
                temp = temp.strip()  # 默认删除两头的空白符（包括'\n', '\r', '\t', ' '）

                line = temp + " = " + 'ChannelReference("' + line.rstrip() + '")\n'
                # i=i.replace('abc','def')   #修改abc为def

            if temp not in para_list:
                para_list.append(temp)
                data.append(line)  # 记录每一行
            else:
                data.append(sec_file + "_" + line)

    # write
    # generate_path = 'DCC111_channel_definition.py'  # 生成通道变量名称
    generate_path = r'{}\test_files\ni_mapping_def.py'.format(project_name)
    with open(generate_path, "w") as f:
        for line in data:
            f.writelines(line)
