def loadModule(module_name):
    """ 传入格式应为 `模块名称[要设置的属性名称=值][...]` """
    from importlib import import_module
    import re
    # 分割名称、属性
    module_property = ''
    if '[' in module_name:
        idx = module_name.index('[')
        module_name, module_property = module_name[:idx], module_name[idx:]

    # 获取模块
    try:
        module = import_module(module_name)
    except:
        return None

    # 设置属性
    for name, value in re.findall(r'\[(.*?)=(.*?)\]', module_property):
        temp_moduel = module
        m = name.split(".")
        name = m[-1]
        for i in m[:-1]:
            temp_moduel = getattr(temp_moduel, i)
        setattr(temp_moduel, name, value)

    return module


def getAuthID():
    from uuid import getnode
    from hashlib import md5

    code1 = int.from_bytes(b"sfe", "big")
    code2 = getnode()
    code = bin(code1 * code2)
    return md5(code.encode()).hexdigest()
