# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\tools\auth.py
# Compiled at: 2018-11-02 11:51:23
# Size of source mod 2**32: 566 bytes
from SFE import getAuthID

def getAuthCode(auth_id=None):
    """ 获取授权码
    - auth_id str[None]: 授权ID, 为`None`时会获取当前机器的ID
    """
    from hashlib import md5
    if auth_id is None:
        auth_id = getAuthID()
    code = 1
    for c in auth_id.replace('f', '').replace('e', '').split('-'):
        if c:
            code *= int(c, 16)

    return md5(bin(code).encode()).hexdigest()


if __name__ == '__main__':
    from fire import Fire
    Fire({'getAuthID':getAuthID, 
     'getAuthCode':getAuthCode})
# okay decompiling tool\auth.pyc
