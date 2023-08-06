"""
This file is used to get information from CodeBeamer.

Please make sure you have REST API access permission of the related project.

@author: siwei.lu
@date: 2023.4.24
"""

import json
import math
import re
import time

import requests
import yaml

from multiprocessing import Process

from ..parse_config_file import parse_config

pattern = re.compile(r'%%\(.*?;\)')

base_yaml_path = '/test_fixture/test_configuration/config.yaml'


class CodeBeamerHandler:
    def __init__(self, project_name, user_name, user_password):
        self.__project_name = project_name
        self.__project_config_path = "{}".format(project_name) + base_yaml_path
        self.__config = parse_config.ConfigHandler(self.__project_config_path)

        self.__project_num = self.__config.get_config_by_name('codebeamer')['project_num']

        self.__hostname = "172.16.200.236:8080"
        self._url_response_time = 0.5
        self.__items_url = "http://{host_name}/cb/rest/category/{project}/items".format(host_name=self.__hostname,
                                                                                        project=self.__project_num)
        self.__name = user_name
        self.__password = user_password

        self.__test_case_info_dict = {}
        self.__case_step_name = []
        self.__parents = []

        self.__project_items = self.get_json_data_from_url(
            '{url}/page/{page}'.format(url=self.__items_url, page=1))  # 获取所有case items
        self.__test_case_items = self.__project_items["items"]
        self._get_all_test_case_ids()

        self.json_data = []
        # self.multi_process()
        self.get_test_cases_info()

    def get_json_data_from_url(self, url, file_name=None):
        data = requests.get(url=url, auth=(self.__name, self.__password))
        json_data = data.json()
        format_json_data = json.loads(data.text)

        if file_name:
            with open(file_name, "w", encoding='utf-8') as file:
                json.dump(format_json_data, file, indent=4, ensure_ascii=False)

        return json_data

    def _get_all_test_case_ids(self):
        total_items = self.__project_items["total"]
        page_size = self.__project_items["size"]
        print("total_items = {}, page_size = {}".format(total_items, page_size))

        for page in range(2, math.ceil(total_items / page_size) + 1):
            project_items = self.get_json_data_from_url('{url}/page/{page}'.format(url=self.__items_url, page=page))
            case_items = project_items["items"]
            self.__test_case_items.extend(case_items)
            time.sleep(self._url_response_time)

        self.__ids = [item['id'] for item in self.__test_case_items]

    def multi_process(self):
        process = []
        for test_case_id in self.__ids:
            process.append(Process(target=self.get_test_case_according_item_id, args=(test_case_id,)))
        [p.start() for p in process]
        [p.join() for p in process]

    def get_test_cases_info(self):
        for test_case_id in self.__ids:
            self._sort_test_case_according_item_id(test_case_id)
            time.sleep(self._url_response_time)  # wait for url response

        for parent in self.__parents:
            case_info_to_yaml_according_parent = []
            for case_info in self.__case_step_name:
                if parent == case_info['case_parent']:
                    case_info_to_yaml_according_parent.append(case_info)

            self.__test_case_info_dict.update({parent: case_info_to_yaml_according_parent})

    def get_test_case_according_item_id(self, test_case_id):
        # cb_case_rul = "http://172.16.200.236:8080/cb/rest/item/{id}".format(id=test_case_id)
        # self.json_data.append(self._get_json_data_from_url(cb_case_rul))
        print(test_case_id, '  ', self.__ids.index(test_case_id))

    def _sort_test_case_according_item_id(self, test_case_id):
        cb_case_rul = "http://172.16.200.236:8080/cb/rest/item/{id}".format(id=test_case_id)
        case_json_data = self.get_json_data_from_url(cb_case_rul)

        if self._check_if_can_auto_test(case_json_data):
            # print("*** {} ***".format(test_case_id))
            case_parent = case_json_data['parent']['name']
            case_name = case_json_data['name']

            description = self.remove_css_pattern(case_json_data['description'])
            test_precondition = self.remove_css_pattern(case_json_data['preAction'])
            case_step, expect_result = self._remove_test_steps_css_pattern(case_json_data['testSteps'])

            sort_case_info_dict = {'case_id': test_case_id,
                                   'description': description,
                                   'preAction': test_precondition,
                                   'testSteps': case_step,
                                   'expect_result': expect_result,
                                   'case_name': case_name,
                                   'case_parent': case_parent}

            self.__case_step_name.append(sort_case_info_dict)
            if case_parent not in self.__parents:
                self.__parents.append(case_parent)

        # rerun {parent: [info,..], ....}

    @staticmethod
    def remove_css_pattern(input_str: str):
        result = re.findall(pattern, input_str)

        if type(result) is list:
            for css_str in result:
                input_str = input_str.replace(css_str, "")
        elif type(result) is str:
            input_str = input_str.replace(result, "")

        input_str = input_str.replace("%!", "").replace(r"\\", "").replace("~", "").replace("\r\n", "")

        return input_str

    @staticmethod
    def _check_if_can_auto_test(case_json_data: dict):
        if 'autoTestable' in case_json_data.keys():
            if case_json_data['autoTestable']['name'] == 'Yes':
                return True
        else:
            return False

    def _remove_test_steps_css_pattern(self, test_case_steps):
        case_step = []
        expect_result = []

        for step in test_case_steps:
            step_0 = step[0].replace("~", "").replace("\r\n", "")  # step: list, step[0]为具体步骤
            expect_result.append(self.remove_css_pattern(step[1]))
            step_0 = self.remove_css_pattern(step_0)
            # print("step = {}\n".format(step_0))
            case_step.append(step_0)

        return case_step, expect_result

    def write_case_to_yaml(self):
        with open("tc_xxx.yaml", "w", encoding='utf-8') as file:
            yaml.dump(self.__test_case_info_dict, file, encoding='utf-8', allow_unicode=True, indent=4)

    def write_case_to_py(self):
        generate_path = r'{}/test_profile/test_case/'.format(self.__project_name)

        for key, values in self.__test_case_info_dict.items():
            py_file_name = self._replace_abnormal_char(key)

            with open(generate_path + "tc_{}.py".format(py_file_name), "w", encoding='utf-8') as file_py:
                file_py.write("# {}\n".format(key))
                for value in values:
                    file_py.write("def test_{}():\n".format(value["case_id"]))
                    file_py.write("    print(\"{}\")\n".format(value["description"]))
                    file_py.write("    # todo:{}: {}\n".format("preAction", value["preAction"]))

                    for i in range(len(value["testSteps"])):
                        file_py.write("    # todo:step_{}: {}\n".format(i + 1, value["testSteps"][i]))

                    for i in range(len(value["expect_result"])):
                        file_py.write("    # todo:expect_result_{}: {}\n".format(i + 1, value["expect_result"][i]))

                    file_py.write('    pass\r\n\n')

    @staticmethod
    def _replace_abnormal_char(input_char: str):
        abnormal_char_list_to_null = [" "]
        abnormal_char_list_to_dash = ["*", "-", "=", "<", ">",
                                      "[", "]", "+", "/", "&",
                                      "%", "(", ")", ",", ".",
                                      ":", "。", ";", "\\", "~",
                                      "∈"]

        for character in abnormal_char_list_to_null:
            input_char = input_char.replace(character, "")

        for character in abnormal_char_list_to_dash:
            input_char = input_char.replace(character, "_")

        return input_char
