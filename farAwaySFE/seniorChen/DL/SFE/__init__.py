# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\__init__.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 981 bytes


def loadModule(module_name):
    """ 传入格式应为 `模块名称[要设置的属性名称=值][...]` """
    from importlib import import_module
    import re
    module_property = ''
    if '[' in module_name:
        idx = module_name.index('[')
        module_name, module_property = module_name[:idx], module_name[idx:]
    try:
        module = import_module(module_name)
    except:
        return

    for name, value in re.findall('\\[(.*?)=(.*?)\\]', module_property):
        temp_moduel = module
        m = name.split('.')
        name = m[-1]
        for i in m[:-1]:
            temp_moduel = getattr(temp_moduel, i)

        setattr(temp_moduel, name, value)

    return module


def getAuthID():
    from uuid import getnode
    from hashlib import md5
    code1 = int.from_bytes(b'sfe', 'big')
    code2 = getnode()
    code = bin(code1 * code2)
    return md5(code.encode()).hexdigest()
# okay decompiling SFE\__init__.pyc
