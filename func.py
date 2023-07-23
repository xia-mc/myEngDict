import load
import easygui as gui
import pie_painter

ui = {
    "title": "我的英语词典",
    "default_msg": "选择一个选项。",
    "default_completed_msg": "已完成操作。",
    "main_ui": {
        "show_choices": ["查询单词", "为词语添加纽带", "历史查询记录", "关闭"],
        "choices": ["查询单词", "为词语添加纽带", "历史查询记录", "关闭", None],
        "functions": ["show_wordenterui", "show_wordenterui_link", "show_searchtimesui", "exit", "exit"]
    },
    "wordenterui": {
        "enter_tips": ["单词"],
        "entering": ["单词", None],
        "functions": ["show_wordshowui", "show_mainui"]
    },
    "wordshowui": {
        "choices": ["好", None],
        "functions": ["show_mainui", "show_mainui"]
    },
    "wordenterui_link": {
        "enter_tips": ["原始单词", "对应的纽带"],
        "entering": [["原始单词", "纽带单词"], None],
        "functions": ["show_completedui_link", "show_mainui"]
    },
    "completedui_link": {
        "choices": ["好", None],
        "functions": ["show_mainui", "show_mainui"]
    },
    "searchtimesui": {
        "choices": [None],
        "functions": ["show_mainui"]
    }
}


def ui_run(ui_iter: dict, ui_input, args: tuple = (), entering: bool = False):
    """
    按照ui字典执行已注册在其中的对应操作。
    遇到非法输入时抛出KeyError。
    :param ui_iter: 在ui字典里的ui子项字典对象。如{"main_ui": ...}
    :param ui_input: 用户在此ui页的输入。
    :param args: 可能的输入参数。
    :param entering: 是否是自由输入模块
    :return: None.
    """
    # 检查是否非法
    if entering is False:
        if ui_input not in ui_iter["choices"]:
            raise KeyError("非法输入。")

    # 执行
    if entering:
        if ui_input is None:  # None时一定为返回
            exec(f'{ui_iter["functions"][1]}()')
        else:
            exec(f'{ui_iter["functions"][0]}{args}')
    else:
        index: int = ui_iter["choices"].index(ui_input)
        exec(f'{ui_iter["functions"][index]}{args}')


def show_mainui():
    try:
        ui_run(
            ui["main_ui"],
            gui.buttonbox(ui["default_msg"], ui["title"], ui["main_ui"]["show_choices"])
        )
    except KeyError:
        show_mainui()


def show_wordenterui():
    try:
        ui_input = gui.multenterbox("", title=ui["title"], fields=ui["wordenterui"]["enter_tips"])
        ui_run(ui["wordenterui"], ui_input, (ui_input,), entering=True)
    except KeyError:
        show_wordenterui()


def show_wordshowui(word: str):
    word = word[0] if word is not str else word  # debug
    # 生成显示的文本
    worddict = load.get_worddict()
    tmp_show: str = f"{word}:\n" \
                    f"    {worddict[word]['mean']}\n\n" \
                    f"    ID:{worddict[word]['code']}\n" \
                    f"    纽带词:{worddict[word]['link']}\n\n" \
                    f"    曾查询此单词{worddict[word]['times']}次"

    # update: 计次
    load.update_worddict(word, "times", worddict[word]['times'] + 1)

    ui_run(
        ui["wordshowui"],
        gui.msgbox(tmp_show, title=ui["title"], ok_button=ui["wordshowui"]["choices"][0])
    )


def show_wordenterui_link():
    """
    用于纽带词的输入GUI
    :return: 无
    """
    try:
        ui_input = gui.multenterbox("Tip: 如果原单词包含纽带，这将覆盖原始内容。", title=ui["title"], fields=ui["wordenterui_link"]["enter_tips"])
        ui_run(ui["wordenterui_link"], ui_input, tuple(ui_input), entering=True)
    except KeyError:
        show_wordenterui()


def show_completedui_link(word: str, doc: str):
    """
    简单的已完成确认窗口。执行link操作
    :return: 无
    """
    # link
    load.update_worddict(word, "link", doc)

    # gui
    ui_run(
        ui["completedui_link"],
        gui.msgbox(ui["default_completed_msg"], title=ui["title"], ok_button=ui["completedui_link"]["choices"][0])
    )


def show_searchtimesui():
    """
    借助PyQT实现的饼状图
    :return: 无
    """
    dic = {
        "从未查阅": 0,
        "查阅一次": 0,
        "<10": 0,
        "<20": 0,
        "<100": 0,
        ">100": 0
    }  # 格式和文案

    # 收集数据
    worddict = load.get_worddict()

    for values in worddict.values():  # 每个values的格式是{"code": , "mean": , "link": , "times": ,}
        times: int = values["times"]  # 查阅次数
        if times < 0:
            raise ValueError(f"编号{values['code']}处的单词拥有错误的查阅次数：{times}")  # debug
        elif times == 1:
            dic["查阅一次"] += 1
        elif times < 10:
            dic["<10"] += 1
        elif times < 100:
            dic["<100"] += 1
        elif times > 100:
            dic[">100"] += 1
        else:
            raise ValueError(f"编号{values['code']}处的单词拥有错误的查阅次数：{times}")  # debug

    # 调用
    pie_painter.run(dic)

    # ui_run
    ui_run(
        ui["searchtimesui"],
        None
    )
