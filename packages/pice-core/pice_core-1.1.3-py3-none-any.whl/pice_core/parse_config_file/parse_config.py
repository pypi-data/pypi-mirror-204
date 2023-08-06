"""
This file is used to parse yaml files and provides some methods.

@Author: Siwei.Lu
@Date: 2022.11.27
"""

import yaml


class ConfigHandler:
    def __init__(self, path):
        """处理配置文件 config.yaml : Absolute Path"""
        self.__config_data = self._parse_config_data(path)

    @staticmethod
    def _parse_config_data(path):
        with open(path, 'r', encoding='UTF-8') as config:
            return yaml.load(config, Loader=yaml.FullLoader)

    def get_config_by_inst(self, inst_type: str):
        return self.__config_data['instrument'][inst_type]

    def get_config_by_name(self, name: str):
        return self.__config_data[name]

    def get_baud_rate(self, inst_type):
        return self.get_config_by_inst(inst_type)['baud_rate']

    def get_com(self, inst_type):
        return self.get_config_by_inst(inst_type)['com']

    def get_dataset_info(self):
        return self.__config_data['dataset']
