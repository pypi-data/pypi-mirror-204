"""
This file is used to parse yaml files of test case.

@Author: Siwei.Lu
@Date: 2022.12.6
"""

import yaml

from .. import logger


class YamlCaseHandler:
    def __init__(self, path=r'\test_profile\test_case\tc_bin.yaml'):
        """处理配置文件"""
        self.__path = path

        try:
            self.__tc_data = self._parse_tc_data(self.__path)
        except BaseException as err:
            print("Read Yaml case failed! \n{}".format(err))
            logger.critical("Read Yaml case failed!\n{}".format(err))

    @staticmethod
    def _parse_tc_data(path):
        with open(path, 'r', encoding='UTF-8') as config:
            return yaml.load(config, Loader=yaml.FullLoader)

    def get_tc_data(self):
        return self.__tc_data

# case = YamlCaseHandler()
# data = case.get_tc_data()
# print(data)
