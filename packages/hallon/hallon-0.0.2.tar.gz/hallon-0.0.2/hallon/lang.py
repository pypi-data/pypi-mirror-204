lang_list = ['en', 'zh']
default_lang = "en"
scripts = {"welcome_msg": ["Hallon Networks Command Line Tools", "汉龙网络命令行工具"],
           "version_msg": ["0.0.1"]
           }


def get_lang_index(l):
    return lang_list.index(l)


def get_lang():
    return lang_list


def get_default_lang():
    return default_lang


def get_msg(msg, l):
    if l in get_lang():
        return scripts[msg][get_lang_index(l)]
    else:
        return get_msg(msg, get_default_lang())

