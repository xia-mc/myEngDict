import json
from typing import Union
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="UTF-8")
RAW_WORDSPACE: str = config["DICT"]["raw_wordsfile"]
WORDSDICT: str = config["DICT"]["wordsfile"]

def get_raw_worddict() -> dict:
    """
    返回一个字典，各单元格式为{单词名称: 翻译}
    旧的方法。
    :return:
    """
    dic = {}

    with open(RAW_WORDSPACE, "r", encoding="UTF-8") as file:
        raw_words = file.readlines()

    for line in raw_words:
        things = line.split("#")  # 例:['1', 'abandon', 'v.抛弃，放弃', '']
        dic.update(
            {things[1]: things[2]}
        )

    return dic


def spawn_newdict_from_raw() -> dict:
    """
    从旧的字典格式，生成json格式的字典。
    新的可扩展词典格式。
    :return: 新的字典结构，可写入json。
    """
    dic = {}

    with open(RAW_WORDSPACE, "r", encoding="UTF-8") as file:
        raw_words = file.readlines()

    for line in raw_words:
        things = line.split("#")  # 例:['1', 'abandon', 'v.抛弃，放弃', '']
        dic.update(
            {
                things[1]: {
                    "code": things[0],
                    "mean": things[2],
                    "link": "",
                    "times": 0
                }
            }
        )

    return dic


def get_worddict() -> dict:
    """
    从新的json格式文件导入到字典。
    格式：
    {
        单词名称: {
            "code": 编号,
            "mean": 含义,
            "link": 联想词,
            "times": 单词被查询次数
        }
    }
    :return: 字典，按照上面的格式
    """
    with open(WORDSDICT, "r", encoding="UTF-8") as file:
        return json.load(file)


def update_worddict(wordname: str, changed_obj: str, value: Union[str, int]) -> None:
    """
    写入修改到json（无文件锁或多线程优化）
    一般修改Link和times（联想词和查询次数）
    :param wordname:
    :param changed_obj:
    :param value:
    :return:
    """
    # 原始
    dic = get_worddict()

    # 修改
    dic[wordname][changed_obj] = value

    # 写入
    with open(WORDSDICT, "w", encoding="UTF=8") as file:
        json.dump(dic, file)
