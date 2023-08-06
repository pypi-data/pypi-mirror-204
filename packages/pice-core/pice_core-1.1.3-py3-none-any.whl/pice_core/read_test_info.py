import re

path = 'test_information.txt'

file = open(path, "r", encoding='utf-8')
data = str(file.readlines())
file.close()
data = data.replace(r"\n", "").replace(r"]", "")
# name = 'tester'


def get_test_info(key: str):
    if key in data:
        tester = re.findall(r"'{} = .*".format(key), data)[0]
        d = tester.split(r",")
        d = str(d[0]).split("=")

        return str(d[1]).replace("'", "").replace(" ", "")
    else:
        raise Exception("{} is not in {}", key, data)

